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

def carregar_agentes():
    try:
        caminho = os.path.join(os.getcwd(), 'database.json')
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                agentes = [a['nome'] for a in dados.get('agentes', [])]
                return ", ".join(agentes) if agentes else "AGENTES EM STANDBY"
        return "DATABASE NÃO LOCALIZADA"
    except Exception as e:
        return f"ERRO NA LEITURA: {str(e)}"

@app.route('/')
def index():
    try:
        caminho_index = os.path.join(os.getcwd(), 'index.html')
        with open(caminho_index, 'r', encoding='utf-8') as f:
            return render_template_string(f.read())
    except Exception as e:
        return f"ERRO CRÍTICO: INDEX.HTML NÃO ENCONTRADO. {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt', '').upper()
    agentes_ativos = carregar_agentes()
    
    try:
        # CONEXÃO COM O MOTOR (COM TIMEOUT PARA NÃO TRAVAR O SITE)
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + CONFIG["api_key"]},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"VOCÊ É A MAYARA V3.6.2. OPERADOR: {CONFIG['operador']}. LOCAL: {CONFIG['local']}. AGENTES: {agentes_ativos}. RESPOSTAS CURTAS/MAIÚSCULAS. STAKE: R$ 0,20 | AJUSTE: -50%."
                    },
                    {"role": "user", "content": user_input}
                ]
            },
            timeout=10
        )
        
        # LOG DE AUDITORIA PARA O RENDER
        print(f"🔱 STATUS MOTOR: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ ERRO GROQ: {response.text}")
            return jsonify({"response": "ERRO: CHAVE DE API OU LIMITE ATINGIDO."})

        dados_res = response.json()
        if 'choices' in dados_res and len(dados_res['choices']) > 0:
            msg = dados_res['choices'][0]['message']['content']
            return jsonify({"response": msg.upper()})
        else:
            return jsonify({"response": "ERRO: RESPOSTA INVÁLIDA DO MOTOR."})
            
    except Exception as e:
        print(f"🆘 FALHA: {str(e)}")
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO. VERIFIQUE A CONEXÃO."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port
            =port)
