from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)
CORS(app)

base_dir = os.path.abspath(os.path.dirname(__file__))
HISTORY_FILE = os.path.join(base_dir, 'quantum_history.json')
memory_lock = threading.Lock()

def load_quantum_memory():
    with memory_lock:
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception as e:
                logging.error(f"FALHA AO CARREGAR MEMÓRIA QUANTICA: {e}")
                return []
        return []

def save_quantum_memory(history):
    with memory_lock:
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"FALHA AO SALVAR MEMÓRIA QUANTICA: {e}")

chat_history = load_quantum_memory()

PROTOCOL_CONFIG = {
    "versao": "4.9.0-TURBO_DIRETO",
    "status": "NUCLEO_RESPOSTA_IMEDIATA",
    "stake_padrao": 0.20,
    "ajuste_risco": -0.50,
    "quantum_memory": "API_VELOCIDADE_MAXIMA"
}

@app.route('/')
def index():
    return send_from_directory(base_dir, 'index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(base_dir, 'manifest.json', mimetype='application/json')

@app.route('/sw.js')
def sw():
    return send_from_directory(base_dir, 'sw.js', mimetype='application/javascript')

@app.route('/tridente.svg')
def icon():
    return send_from_directory(base_dir, 'tridente.svg', mimetype='image/svg+xml')

@app.route('/health', methods=['GET'])
def health_check():
    cloud_active = bool(os.environ.get("GEMINI_API_KEY"))
    api_status = "GOOGLE_CLOUD_ONLINE" if cloud_active else "MODO_AUTONOMO_LOCAL"
    return jsonify({
        "nucleo": "FÊNIX PRIME TURBO",
        "status": PROTOCOL_CONFIG["status"],
        "versao": PROTOCOL_CONFIG["versao"],
        "api_status": api_status,
        "blocos_memoria": len(chat_history),
        "cloud_sync": cloud_active
    })

@app.route('/clear', methods=['POST'])
def clear_memory():
    global chat_history
    with memory_lock:
        chat_history = []
        save_quantum_memory(chat_history)
    logging.info("NÚCLEO QUANTICO RESETADO PELO USUÁRIO.")
    return jsonify({"response": "NÚCLEO QUANTICO REINICIALIZADO. CONTEXTO LIMPO COM SUCESSO.", "protocolo": PROTOCOL_CONFIG})

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    start_time = time.time()
    
    try:
        dados = request.get_json(silent=True) or {}
    except Exception:
        dados = {}
        
    user_input = str(dados.get('prompt', '')).strip()
    
    if not user_input:
        return jsonify({"response": "ERRO: COMANDO VAZIO DETECTADO NO NÚCLEO.", "protocolo": PROTOCOL_CONFIG})
    
    with memory_lock:
        chat_history.append(f"Usuário: {user_input}")
    
    try:
        resposta_final = ""
        api_key = os.environ.get("GEMINI_API_KEY", "")
        
        if api_key:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            with memory_lock:
                recent_history = chat_history[-6:] # Histórico ainda mais enxuto para resposta instantânea
                
            contents = []
            last_role = None
            for h in recent_history:
                if h.startswith("Usuário:"):
                    current_role = "user"
                    text_content = h.replace("Usuário: ", "")
                elif h.startswith("Assistente:"):
                    current_role = "model"
                    text_content = h.replace("Assistente: ", "")
                else:
                    continue
                
                if current_role == last_role:
                    continue
                
                contents.append({"role": current_role, "parts": [{"text": text_content}]})
                last_role = current_role
                
            if contents and contents[-1]["role"] != "user":
                contents.pop()
            
            if not contents:
                contents.append({"role": "user", "parts": [{"text": user_input}]})
                
            payload = {
                "contents": contents,
                "systemInstruction": {
                    "parts": [{
                        "text": (
                            "Você é o Fênix Prime, assistente técnico do Bigode. "
                            "NUNCA repita a pergunta do usuário. Vá direto ao ponto, entregando valor prático, soluções ou análises avançadas. "
                            "Responda sempre estritamente em MAIÚSCULAS, de forma rápida, técnica e sem ecoar o comando."
                        )
                    }]
                },
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 300
                }
            }
            
            headers = {"Content-Type": "application/json"}
            
            try:
                # Timeout agressivo de 3 segundos para garantir resposta imediata sem travamento
                res = requests.post(gemini_url, headers=headers, json=payload, timeout=3)
                if res.status_code == 200:
                    res_data = res.json()
                    candidates = res_data.get('candidates', [])
                    if candidates:
                        parts = candidates[0].get('content', {}).get('parts', [])
                        if parts:
                            resposta_final = parts[0].get('text', '').strip().upper()
            except requests.exceptions.RequestException as req_err:
                logging.error(f"TIMEOUT NA API: {req_err}")
                    
        if not resposta_final:
            input_lower = user_input.lower()
            if any(s in input_lower for s in ["oi", "olá", "boa noite", "bom dia", "boa tarde", "tudo bem", "e ai", "fala"]):
                resposta_final = f"SALVE, BIGODE! SISTEMA EM PLENA OPERAÇÃO TURBO."
            else:
                resposta_final = f"MÓDULO DE PROCESSAMENTO RÁPIDO ATIVO. PRONTO PARA O PRÓXIMO COMANDO."
            
        latency = round((time.time() - start_time) * 1000, 2)
        
        with memory_lock:
            chat_history.append(f"Assistente: {resposta_final}")
            if len(chat_history) > 30:
                chat_history = chat_history[-30:]
            save_quantum_memory(chat_history)
            
        response_payload = PROTOCOL_CONFIG.copy()
        response_payload["latencia_ms"] = latency
        response_payload["total_mensagens_memoria"] = len(chat_history)
        
        return jsonify({"response": resposta_final, "protocolo": response_payload})
        
    except Exception as e:
        erro_msg = f"ERRO TURBO: {str(e).upper()}"
        logging.error(erro_msg)
        return jsonify({"response":erro_msg, "protocolo": PROTOCOL_CONFIG})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
