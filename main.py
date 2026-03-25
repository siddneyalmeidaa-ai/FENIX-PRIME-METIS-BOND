from flask import Flask, render_template_string, request, jsonify
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
    "api_key": "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"
}

# --- FUNÇÃO DE LEITURA DO MOTOR (DATABASE) ---
def carregar_agentes():
    try:
        # BUSCA O ARQUIVO NO DIRETÓRIO ATUAL DO RENDER
        caminho = os.path.join(os.getcwd(), 'database.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            agentes = [a['nome'] for a in dados.get('agentes', [])]
            return ", ".join(agentes) if agentes else "NENHUM AGENTE LOCALIZADO"
    except Exception as e:
        return f"ERRO NA LEITURA: {str(e)}"

# --- INTERFACE VISUAL INTEGRAL V3.6.2 ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8-SIG">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Fênix Prime - S.A. SUPREMACIA</title>
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            background-color: #131314; color: #e3e3e3; font-family: 'Segoe UI', sans-serif; 
            margin: 0; display: flex; flex-direction: column; height: 100dvh; overflow: hidden; 
        }
        header { 
            padding: 45px 20px 15px; font-weight: bold; border-bottom: 1px solid #444746; 
            display: flex; align-items: center; justify-content: space-between; background: #1e1f20; 
        }
        .status-dot { width: 12px; height: 12px; background: #00ff00; border-radius: 50%; box-shadow: 0 0 12px #00ff00; }
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .message { max-width: 85%; padding: 12px 16px; border-radius: 18px; font-size: 14px; line-height: 1.5; word-wrap: break-word; }
        .ai-msg { align-self: flex-start; background-color: #1e1f20; border: 1px solid #444746; border-bottom-left-radius: 4px; }
        .user-msg { align-self: flex-end; background-color: #2b2a33; border-bottom-right-radius: 4px; color: #fff; }
        .tag-ai { color: #8ab4f8; font-size: 10px; font-weight: bold; display: block; margin-bottom: 5px; }
        .monitor-soberania { background: #1e1f20; padding: 12px; border: 1px solid #33CC33; border-radius: 8px; margin: 10px 20px; font-family: monospace; border-left: 4px solid #33CC33; }
        .monitor-grid { color: #e3e3e3; font-size: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 5px; }
        .input-wrapper { 
            padding: 15px 20px; background: #131314; 
            padding-bottom: calc(25px + env(safe-area-inset-bottom)); 
        }
        .input-box { max-width: 800px; margin: 0 auto; background: #1e1f20; border: 1px solid #444746; border-radius: 28px; display: flex; align-items: center; padding: 5px 15px; gap: 10px; }
        .btn-sensor { background: none; border: none; color: #8ab4f8; font-size: 20px; cursor: pointer; padding: 0 5px; }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px; font-size: 16px; outline: none; }
        .btn-exe { background: #8ab4f8; color: #000; border: none; border-radius: 20px; padding: 8px 20px; cursor: pointer; font-weight: bold; }
        .footer-text { text-align: center; font-size: 10px; color: #8e918f; margin-top: 8px; text-transform: uppercase; }
    </style>
</head>
<body>
    <header>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div class="status-dot"></div>
            <span>FÊNIX PRIME: <span style="color:#00ff00">LIBERADO (1)</span></span>
        </div>
        <div style="font-size: 12px; color: #8ab4f8;">V3.6.2 | 2026</div>
    </header>
    <div id="chat-container"></div>
    <div class="monitor-soberania">
        <div class="monitor-grid">
            <div>ESTABILIDADE PWA: <span style="color: #33CC33;">● ATIVO</span></div>
            <div>QUANTUM MEMORY: <span style="color: #33CC33;">● SINCRO</span></div>
            <div>PROTOCOLO IPI: <span style="color: #33CC33;">● R$ 0,20</span></div>
            <div>AJUSTE RISCO: <span style="color: #33CC33;">● -50%</span></div>
        </div>
    </div>
    <div class="input-wrapper">
        <div class="input-box">
            <button class="btn-sensor">📎</button>
            <button class="btn-sensor">🎤</button>
            <input type="text" id="in" placeholder="Comando para os Agentes..." autocomplete="off">
            <button class="btn-exe" onclick="enviar()">EXE</button>
        </div>
        <div class="footer-text">PROTOCOLO IPI | STAKE R$ 0,20 | TABOÃO DA SERRA</div>
    </div>
    <script>
        async function enviar() {
            const input = document.getElementById('in');
            const text = input.value.trim();
            if(!text) return;
            const idU = "u_" + Date.now();
            addMsg(text, 'user-msg', idU);
            input.value = '';
            const idAi = "ai_" + Date.now();
            addMsg("PROCESSANDO...", 'ai-msg', idAi);
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                });
                const data = await res.json();
                document.getElementById(idAi).innerHTML = `<span class="tag-ai">🔱 FÊNIX V3.6.2</span>` + data.response;
            } catch (e) {
                document.getElementById(idAi).innerText = "ERRO NA MATRIZ V3.6.2: SERVIDOR OFFLINE.";
            }
        }
        function addMsg(t, c, id) {
            const d = document.createElement('div');
            d.className = `message ` + c;
            if(id) d.id = id;
            const tag = c === 'ai-msg' ? '<span class="tag-ai">🔱 FÊNIX V3.6.2</span>' : '';
            d.innerHTML = tag + t.toUpperCase();
            document.getElementById('chat-container').appendChild(d);
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
        }
        window.onload = () => addMsg("SOBERANIA V3.6.2 ATIVA. ARQUITETO BIGODE DETECTADO.", "ai-msg");
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt', '').upper()
    
    # LEITURA DOS AGENTES PARA CONTEXTO DA IA
    agentes_ativos = carregar_agentes()
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + CONFIG["api_key"]},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"VOCÊ É A MAYARA V3.6.2. OPERADOR: BIGODE. LOCAL: {CONFIG['local']}. AGENTES DISPONÍVEIS: {agentes_ativos}. RESPOSTAS CURTAS E EM MAIÚSCULAS. USE SEMPRE R$ 0,20 E AJUSTE -50%."
                    },
                    {"role": "user", "content": user_input}
                ]
            }
        )
        msg = response.json()['choices'][0]['message']['content']
        return jsonify({"response": msg.upper()})
    except Exception:
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO V3.6.2. VERIFIQUE A CONEXÃO."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
