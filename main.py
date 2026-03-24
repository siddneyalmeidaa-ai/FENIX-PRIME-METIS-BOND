from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURAÇÕES DE SOBERANIA ---
CONFIG = {
    "operador": "BIGODE",
    "versao": "3.6.2",
    "local": "TABOÃO DA SERRA, SP",
    "api_key": "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"
}

# --- INTERFACE VISUAL (O SEU HTML INTEGRADO) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fênix Prime - S.A. SUPREMACIA</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #131314; color: #e3e3e3; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        header { padding: 40px 20px 15px; font-weight: bold; border-bottom: 1px solid #444746; display: flex; align-items: center; justify-content: space-between; background: #1e1f20; }
        .status-dot { width: 12px; height: 12px; background: #00ff00; border-radius: 50%; box-shadow: 0 0 12px #00ff00; }
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .message { max-width: 85%; padding: 12px 16px; border-radius: 18px; font-size: 15px; line-height: 1.5; }
        .user-msg { align-self: flex-end; background-color: #2b2a33; border-bottom-right-radius: 4px; }
        .ai-msg { align-self: flex-start; background-color: #1e1f20; border: 1px solid #444746; border-bottom-left-radius: 4px; }
        .input-wrapper { padding: 20px 20px 40px; background: #131314; }
        .input-box { max-width: 800px; margin: 0 auto; background: #1e1f20; border: 1px solid #444746; border-radius: 28px; display: flex; padding: 5px 15px; }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px; outline: none; }
        button { background: #8ab4f8; border: none; border-radius: 20px; padding: 0 20px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div class="status-dot"></div>
            <span>FÊNIX PRIME: <span style="color:#00ff00">LIBERADO (1)</span></span>
        </div>
        <div style="font-size: 12px; color: #8ab4f8;">QUANTUM ENGINE 2026</div>
    </header>
    <div id="chat-container"></div>
    <div class="input-wrapper">
        <div class="input-box">
            <input type="text" id="in" placeholder="Comando para os Agentes..." autocomplete="off">
            <button onclick="enviar()">EXE</button>
        </div>
    </div>
    <script>
        async function enviar() {
            const input = document.getElementById('in');
            const text = input.value.trim();
            if(!text) return;
            addMsg(text, 'user-msg');
            input.value = '';
            
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: text})
            });
            const data = await res.json();
            addMsg(data.response, 'ai-msg');
        }
        function addMsg(t, c) {
            const d = document.createElement('div');
            d.className = `message ${c}`;
            d.innerText = t;
            document.getElementById('chat-container').appendChild(d);
            document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt').upper()
    
    # LÓGICA DA GROQ INTEGRADA NO PYTHON
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {CONFIG['api_key']}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": f"VOCÊ É A MAYARA V3.6.2. OPERADOR: {CONFIG['operador']}. LOCAL: {CONFIG['local']}. DATA: 24/03/2026. RESPOSTAS EM MAIÚSCULAS E SINCERAS."},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        msg = response.json()['choices'][0]['message']['content']
        return jsonify({"response": msg.upper()})
    except:
        return jsonify({"response": "ERRO NO MOTOR QUÂNTICO."})

if __name__ == '__main__':
    app.run(debug=
            True)
