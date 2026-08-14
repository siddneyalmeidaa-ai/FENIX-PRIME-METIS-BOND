from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

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

@app.route('/chat', methods=['POST'])
def chat():
    try:
        dados = request.get_json() or {}
        user_input = dados.get('prompt', '').upper()
        
        # RESPOSTAS DINÂMICAS BASEADAS NO COMANDO DO ARQUITETO SIDNEY
        if "BOM" in user_input or "NOITE" in user_input or "DIA" in user_input:
            resposta_final = "BOA NOITE, ARQUITETO SIDNEY. SISTEMA SOBERANO TOTALMENTE OPERACIONAL."
        elif "COMO" in user_input and "ESTA" in user_input:
            resposta_final = "ESTABILIDADE MÁXIMA. PROTOCOLO IPI ATIVO E MOTORES QUÂNTICOS SINCRONIZADOS."
        elif "NOVIDADE" in user_input:
            resposta_final = "TODAS AS BLINDAGENS DO SERVIDOR ESTÃO ATIVAS E O PWA OPERA COM SOBERANIA."
        else:
            resposta_final = f"COMANDO RECEBIDO COM SUCESSO: {user_input} | SOBERANIA ATIVA."
        
        return jsonify({"response": resposta_final})
    except Exception as e:
        return jsonify({"response": "MOTOR QUÂNTICO ESTABILIZADO. SOBERANIA ATIVA."})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
