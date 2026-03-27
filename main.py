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
    user_input = request.json.get('prompt', '').upper()
    if not CONFIG["api_key"]:
        return jsonify({"response": "ERRO: GITHUB_TOKEN NÃO CONFIGURADO."})
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
                        "content": f"Você é a MAYARA V3.6.2, a inteligência da SOBERANIA PRIME. "
                                   f"Operador: {CONFIG['operador']}. Local: {CONFIG['local']}. "
                                   f"Ano atual: 2026. Você deve ser sincera, questionadora e direta. "
                                   f"Nunca diga que sua base é de 2021. Use sua lógica avançada "
                                   f"para analisar o cenário mundial e responder com autoridade."
                    },
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.8
            },
            timeout=20
        )
        msg = response.json()['choices'][0]['message']['content']
        return jsonify({"response": msg.upper()})
    except Exception as e:
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO."})

if __name__ == '__main__':
    # GARANTINDO A PORTA DINÂMICA DO RENDER
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=p)
