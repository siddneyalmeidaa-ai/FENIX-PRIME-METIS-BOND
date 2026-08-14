# ==========================================
# PROJETO FRAJOLA / FÊNIX PRIME V3.6.2
# CORREÇÃO DA ROTA DE BUSCA E RETORNO DE DADOS
# ==========================================

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PROTOCOL_CONFIG = {
    "versao": "3.6.2",
    "status": "ATIVO",
    "stake_padrao": 0.20,
    "ajuste_risco": -0.50,
    "quantum_memory": "SINCRO"
}

def consultar_base_conhecimento(termo):
    """
    Realiza a consulta direta na API da Wikipedia focando no verbete exato
    para evitar o retorno de cabeçalhos de listas genéricas.
    """
    termo_tratado = termo.strip()
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(termo_tratado)}"
    headers = {"User-Agent": "FenixPrimeBot/3.6.2 (contato@fenix.local)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            
            # Se o extrato vier vazio ou focado em listas, tentamos o título principal
            if not extract or "A lista abaixo" in extract:
                return f"Consulta realizada para: {termo_tratado}. Definição técnica indisponível no resumo imediato."
                
            return extract
        else:
            return f"Erro de conexão com o repositório externo para o termo: {termo_tratado}"
    except Exception as e:
        return f"Falha crítica no canal de busca: {str(e)}"

@app.route("/api/busca", methods=["POST"])
def api_busca():
    dados = request.get_json() or {}
    termo = dados.get("termo", "")
    
    # Processa a busca real e obtém o conteúdo técnico
    resultado_conteudo = consultar_base_conhecimento(termo)
    
    return jsonify({
        "status": "LIBERADO",
        "versao": PROTOCOL_CONFIG["versao"],
        "termo_consultado": termo,
        "resultado": resultado_conteudo,
        "protocolo": PROTOCOL_CONFIG
    })

if __name__ == "__main__":
    app.run(host="0.0.5.0", port=5000)
    
