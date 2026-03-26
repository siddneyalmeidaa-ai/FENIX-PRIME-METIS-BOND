from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
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

@app.route('/')
def index():
    try:
        # Entrega o index.html da raiz para evitar o erro Not Found
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f"ERRO CRÍTICO: INDEX.HTML NÃO ENCONTRADO. {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt', '').upper()
    
    if not CONFIG["api_key"]:
        return jsonify({"response": "ERRO: GITHUB_TOKEN NÃO CONFIGURADO NO RENDER."})
    
    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {CONFIG['api_key']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            f"VOCÊ É A MAYARA V3.6.2. OPERADOR: {CONFIG['operador']}. LOCAL: {CONFIG['local']}. "
                            f"RESPOSTAS CURTAS/MAIÚSCULAS. HOJE É 26/03/2026. "
                            f"VOCÊ É UMA FORTALEZA DE DADOS. NUNCA ESCREVA 'FORTEZA', O CORRETO É 'FORTALEZA'."
                        )
                    },
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7
            },
            timeout=20
        )
        
        dados_res = response.json()
        msg = dados_res['choices'][0]['message']['content']
        return jsonify({"response": msg.upper()})
            
    except Exception as e:
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO. VERIFIQUE O RENDER."})

if __name__ == '__main__':
    # PORTA CONFIGURADA EM LINHA ÚNICA - SEM ERRO DE SINTAXE - DINASTIA Y
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p
            ort)
