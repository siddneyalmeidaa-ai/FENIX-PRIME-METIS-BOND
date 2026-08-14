from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

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

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json() or {}
    user_input = dados.get('prompt', '').upper()
    
    if not CONFIG["api_key"]:
        return jsonify({"response": f"COMANDO SOBERANO EXECUTADO: {user_input} | ARQUITETO SIDNEY"})
    
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
                        "content": f"Você é a FÊNIX PRIME V3.6.2, inteligência soberana. Operador: {CONFIG['operador']}. Responda de forma direta, clara e inteligente em letras maiúsculas."
                    },
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7
            },
            timeout=15
        )
        res_json = response.json()
        if 'choices' in res_json and len(res_json['choices']) > 0:
            msg = res_json['choices'][0]['message']['content']
            return jsonify({"response": msg.upper()})
        else:
            return jsonify({"response": f"PROCESSADO COM SUCESSO: {user_input}"})
    except Exception as e:
        return jsonify({"response": f"MODO SOBERANO ATIVO PARA: {user_input}"})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
