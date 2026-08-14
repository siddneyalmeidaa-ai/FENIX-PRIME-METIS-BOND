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
        # Passo 1: Busca inteligente por termos relacionados na Wikipedia em português
        search_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(user_input)}&format=json"
        headers = {"User-Agent": "FenixPWA/3.6.2"}
        search_res = requests.get(search_url, headers=headers, timeout=10)
        
        if search_res.status_code == 200:
            search_data = search_res.json()
            results = search_data.get('query', {}).get('search', [])
            
            if results:
                # Pega o título do primeiro artigo encontrado na busca
                best_title = results[0]['title']
                summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_title)}"
                sum_res = requests.get(summary_url, headers=headers, timeout=10)
                
                if sum_res.status_code == 200:
                    sum_data = sum_res.json()
                    extract = sum_data.get('extract')
                    if extract:
                        return jsonify({"response": extract.upper()})
        
        return jsonify({"response": f"CONSULTA EXECUTADA PARA '{user_input.upper()}': NENHUM ARTIGO CORRESPONDENTE LOCALIZADO NA BASE GLOBAL."})
    except Exception as e:
        return jsonify({"response": f"ERRO NA EXECUÇÃO DA BUSCA: {str(e).upper()}"})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
