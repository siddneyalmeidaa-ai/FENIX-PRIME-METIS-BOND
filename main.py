from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES DE SOBERANIA V3.6.2 ---
CONFIG = {
    "operador": "BIGODE",
    "versao": "3.6.2",
    "local": "TABOÃO DA SERRA, SP",
    "api_key": os.environ.get("GITHUB_TOKEN")
}

base_dir = os.path.abspath(os.path.dirname(__file__))

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

# --- MOTOR DE INTELIGÊNCIA RECALIBRADO (MODO SOBERANO) ---

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json() or {}
    user_input = dados.get('prompt', '').upper()
    historico_cliente = dados.get('context', [])
    
    if not CONFIG["api_key"]:
        return jsonify({"response": "ERRO: GITHUB_TOKEN NÃO CONFIGURADO."})
    try:
        # CONSTRÓI AS MENSAGENS INCLUINDO O CONTEXTO ACUMULATIVO DA QUANTUM MEMORY
        mensagens = [
            {
                "role": "system", 
                "content": f"Você é a FÊNIX PRIME V3.6.2, a inteligência da SOBERANIA PRIME. "
                           f"Operador: {CONFIG['operador']}. Local: {CONFIG['local']}. "
                           f"Ano atual: 2026. Regra acumulativa e soberana ativa."
            }
        ]
        
        # ADICIONA O HISTÓRICO PARA GARANTIR A SINCRONIZAÇÃO QUÂNTICA
        for h in historico_cliente[-10:]:
            papel = "user" if h.get("classe") == "user-msg" else "assistant"
            mensagens.append({"role": papel, "content": h.get("txt", "")})
            
        mensagens.append({"role": "user", "content": user_input})

        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {CONFIG['api_key']}", 
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": mensagens,
                "temperature": 0.8
            },
            timeout=20
        )
        
        res_json = response.json()
        if 'choices' in res_json and len(res_json['choices']) > 0:
            msg = res_json['choices'][0]['message']['content']
            return jsonify({"response": msg.upper()})
        else:
            return jsonify({"response": "SOBERANIA ATIVA. COMANDO PROCESSADO."})
            
    except Exception as e:
        return jsonify({"response": "MOTOR QUÂNTICO ESTABILIZADO. SOBERANIA ATIVA."})

if __name__ == '__main__':
    # GARANTINDO A PORTA DINÂMICA DO RENDER
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
