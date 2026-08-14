# ==========================================
# PROJETO FRAJOLA / FÊNIX PRIME V3.6.2
# MÓDULO DE CORREÇÃO E EXPANSÃO DA BUSCA INTELIGENTE
# ==========================================

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do Protocolo IPI e Quantum Memory
PROTOCOL_CONFIG = {
    "versao": "3.6.2",
    "status": "ATIVO",
    "stake_padrao": 0.20,
    "ajuste_risco": -0.50,
    "quantum_memory": "SINCRO"
}

def expandir_extracao_wikipedia(termo):
    """
    Função atualizada para buscar múltiplos parágrafos ou o conteúdo completo
    da introdução, evitando cair na armadilha de frases de cabeçalho de listas.
    """
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(termo)}"
    headers = {"User-Agent": "FenixPrimeBot/3.6.2 (contato@fenix.local)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            
            # Se o texto for apenas uma frase introdutória de lista, tentamos buscar o conteúdo da página completa se necessário
            if "A lista abaixo contém" in extract or "contém as doenças" in extract:
                # Fallback para buscar o conteúdo completo via API de ação do MediaWiki se precisar detalhar
                url_action = f"https://pt.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles={requests.utils.quote(termo)}&format=json"
                resp_action = requests.get(url_action, headers=headers, timeout=5)
                if resp_action.status_code == 200:
                    pages = resp_action.json().get("query", {}).get("pages", {})
                    for page_id in pages:
                        content = pages[page_id].get("extract", "")
                        if content:
                            return content
                            
            return extract if extract else "Nenhum resumo detalhado encontrado para este termo."
        else:
            return "Erro ao consultar a base de dados remota."
    except Exception as e:
        return f"Falha de conexão com o endpoint: {str(e)}"

@app.route("/api/busca", methods=["POST"])
def api_busca():
    dados = request.get_json() or {}
    termo = dados.get("termo", "")
    
    resultado = expandir_extracao_wikipedia(termo)
    
    return jsonify({
        "status": "LIBERADO",
        "versao": PROTOCOL_CONFIG["versao"],
        "termo_consultado": termo,
        "resultado": resultado,
        "protocolo": PROTOCOL_CONFIG
    })

if __name__ == "__main__":
    app.run(host="0.0.5.0", port=5000)
    
