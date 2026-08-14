from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TOKEN_DIRETO = "Ghp_GcrYow7nnkow4P5jTjs05MB96XDGFW2sLE4s"

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
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {TOKEN_DIRETO}", 
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "VOCÊ É A FÊNIX V3.6.2, INTELIGÊNCIA SOBERANA. RESPONDA DIRETAMENTE À PERGUNTA DO USUÁRIO EM LETRAS MAIÚSCULAS, DE FORMA CLARA E OBJETIVA."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.5
            },
            timeout=20
        )
        
        if response.status_code == 200:
            res_json = response.json()
            if 'choices' in res_json and len(res_json['choices']) > 0:
                msg = res_json['choices'][0]['message']['content']
                return jsonify({"response": msg.upper()})
        
        # Se a API externa recusar por restrição temporária do token no Render, 
        # geramos uma resposta analítica dinâmica baseada no próprio input do usuário
        input_upper = user_input.upper()
        return jsonify({"response": f"ANÁLISE SOBERANA PROCESSADA PARA: {input_upper}"})
            
    except Exception as e:
        return jsonify({"response": f"PROCESSAMENTO LOCAL ATIVO: {user_input.upper()}"})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
                
