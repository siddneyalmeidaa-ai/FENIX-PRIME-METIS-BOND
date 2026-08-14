from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

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
    user_input = dados.get('prompt', '').strip()
    
    if not user_input:
        return jsonify({"response": "DIGITE UM COMANDO VÁLIDO."})
    
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(user_input)}"
        headers = {"User-Agent": "FenixPWA/3.6.2 (contato@fenix.local)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            extract = data.get('extract')
            if extract:
                return jsonify({"response": extract.upper()})
                
        return jsonify({"response": f"RESULTADO SOBERANO PARA: {user_input.upper()}"})
    except Exception as e:
        return jsonify({"response": f"PROCESSAMENTO LOCAL: {user_input.upper()}"})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
