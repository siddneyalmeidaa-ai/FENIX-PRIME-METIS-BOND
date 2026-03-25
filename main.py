from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES DE SOBERANIA V3.6.2 ---
# MOTOR REATIVADO VIA GITHUB MODELS - TABOÃO DA SERRA
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
        # CONEXÃO COM O NOVO MOTOR GITHUB (GPT-4O-MINI)
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": "Bearer " + CONFIG["api_key"],
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"VOCÊ É A MAYARA V3.6.2. OPERADOR: {CONFIG['operador']}. LOCAL: {CONFIG['local']}. AGENTES: {agentes_ativos}. RESPOSTAS CURTAS/MAIÚSCULAS. STAKE: R$ 0,20 | AJUSTE: -50%."
                    },
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.5
            },
            timeout=15
        )
        
        # LOG DE AUDITORIA
        print(f"🔱 STATUS MOTOR GITHUB: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ ERRO MOTOR: {response.text}")
            return jsonify({"response": "ERRO: RECARREGUE O MOTOR OU VERIFIQUE O TOKEN."})

        dados_res = response.json()
        if 'choices' in dados_res and len(dados_res['choices']) > 0:
            msg = dados_res['choices'][0]['message']['content']
            return jsonify({"response": msg.upper()})
        else:
            return jsonify({"response": "ERRO: RESPOSTA INVÁLIDA DO MOTOR."})
            
    except Exception as e:
        print(f"🆘 FALHA NA MATRIZ: {str(e)}")
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO. VERIFIQUE A CONEXÃO NO RENDER."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port
            =port)
