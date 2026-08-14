from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.abspath(os.path.dirname(__file__))

# Quantum Memory local para manter o contexto do diálogo ativo
chat_history = []

PROTOCOL_CONFIG = {
    "versao": "3.6.2",
    "status": "ATIVO",
    "stake_padrao": 0.20,
    "ajuste_risco": -0.50,
    "quantum_memory": "SINCRO"
}

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
    global chat_history
    dados = request.get_json() or {}
    user_input = dados.get('prompt', '').strip()
    
    if not user_input:
        return jsonify({"response": "DIGITE UM COMANDO VÁLIDO.", "protocolo": PROTOCOL_CONFIG})
    
    # Adiciona a entrada do usuário ao histórico para manter o contexto
    chat_history.append(f"Usuário: {user_input}")
    
    try:
        # Se a pergunta for uma continuação (ex: "fale mais sobre isso"), usamos o contexto anterior
        termo_busca = user_input
        if len(user_input.split()) <= 3 and len(chat_history) > 2:
            # Pega o termo principal discutido anteriormente para dar continuidade
            termo_busca = chat_history[-3].replace("Usuário: ", "")

        # Busca inteligente na Wikipedia
        search_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(termo_busca)}&format=json"
        headers = {"User-Agent": "FenixPWA/3.6.2"}
        search_res = requests.get(search_url, headers=headers, timeout=10)
        
        resposta_final = ""
        if search_res.status_code == 200:
            search_data = search_res.json()
            results = search_data.get('query', {}).get('search', [])
            
            if results:
                best_title = results[0]['title']
                summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_title)}"
                sum_res = requests.get(summary_url, headers=headers, timeout=10)
                
                if sum_res.status_code == 200:
                    sum_data = sum_res.json()
                    extract = sum_data.get('extract')
                    if extract:
                        resposta_final = extract.upper()
        
        if not resposta_final:
            resposta_final = f"CONSULTA EXECUTADA PARA '{user_input.upper()}': NENHUM ARTIGO CORRESPONDENTE LOCALIZADO NA BASE GLOBAL."
            
        # Salva a resposta no histórico da Quantum Memory
        chat_history.append(f"Assistente: {resposta_final}")
        
        # Mantém apenas as últimas 10 interações para não estourar a memória
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
            
        return jsonify({"response": resposta_final, "protocolo": PROTOCOL_CONFIG})
        
    except Exception as e:
        erro_msg = f"ERRO NA EXECUÇÃO DA BUSCA: {str(e).upper()}"
        return jsonify({"response": erro_msg, "protocolo": PROTOCOL_CONFIG})

if __name__ == '__main__':
    p = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=p)
    
