from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÕES DE SOBERANIA V3.6.2 ---
CONFIG = {
    "operador": "BIGODE",
    "versao": "3.6.2",
    "local": "TABOÃO DA SERRA, SP"
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

# --- MOTOR DE INTELIGÊNCIA SOBERANO LOCAL ---

@app.route('/chat', methods=['POST'])
def chat():
    try:
        dados = request.get_json() or {}
        user_input = dados.get('prompt', '').upper()
        
        # PROCESSAMENTO SOBERANO E IMEDIATO
        resposta_final = f"COMANDO SOBERANO EXECUTADO: {user_input} | ARQUITETO SIDNEY"
        
        return jsonify({"response": resposta_final})
    except Exception as e:
        return jsonify({"response": "MOTOR QUÂNTICO ESTABILIZADO. SOBERANIA ATIVA."})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
