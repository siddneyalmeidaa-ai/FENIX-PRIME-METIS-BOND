from flask import Flask, render_template_string, request, jsonify
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
    "api_key": "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"
}

# --- MOTOR DE BUSCA DOS 17 AGENTES ---
def carregar_agentes():
    try:
        # BUSCA O ARQUIVO DATABASE NA RAIZ DO RENDER
        caminho = os.path.join(os.getcwd(), 'database.json')
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                agentes = [a['nome'] for a in dados.get('agentes', [])]
                return ", ".join(agentes) if agentes else "AGENTES EM STANDBY"
        return "DATABASE NÃO LOCALIZADA"
    except Exception as e:
        return f"ERRO NA LEITURA: {str(e)}"

# --- ROTA DA INTERFACE (RAIZ) ---
@app.route('/')
def index():
    try:
        # LÊ O INDEX.HTML DIRETAMENTE DA RAIZ DO REPOSITÓRIO
        caminho_index = os.path.join(os.getcwd(), 'index.html')
        with open(caminho_index, 'r', encoding='utf-8') as f:
            return render_template_string(f.read())
    except Exception as e:
        return f"ERRO CRÍTICO: ARQUIVO INDEX.HTML NÃO ENCONTRADO NA RAIZ. {str(e)}"

# --- ROTA DE COMUNICAÇÃO (MOTOR) ---
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt', '').upper()
    
    # SINCRONIZAÇÃO DOS AGENTES PARA O CONTEXTO
    agentes_ativos = carregar_agentes()
    
    try:
        # CONEXÃO COM O MOTOR DE INTELIGÊNCIA (GROQ/LLAMA)
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + CONFIG["api_key"]},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"VOCÊ É A MAYARA V3.6.2. OPERADOR: {CONFIG['operador']}. LOCAL: {CONFIG['local']}. AGENTES DISPONÍVEIS: {agentes_ativos}. RESPOSTAS SEMPRE CURTAS E EM MAIÚSCULAS. PROTOCOLO IPI: R$ 0,20. AJUSTE DE RISCO: -50%."
                    },
                    {"role": "user", "content": user_input}
                ]
            }
        )
        dados_res = response.json()
        if 'choices' in dados_res:
            msg = dados_res['choices'][0]['message']['content']
            return jsonify({"response": msg.upper()})
        else:
            return jsonify({"response": "ERRO: RESPOSTA INVÁLIDA DO MOTOR."})
            
    except Exception:
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO V3.6.2. VERIFIQUE A CONEXÃO."})

if __name__ == '__main__':
    # PORTA 5000 PADRÃO PARA O RENDER
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=
            port)
