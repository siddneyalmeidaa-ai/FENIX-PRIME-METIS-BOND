<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fênix Prime - S.A. SUPREMACIA</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #131314; color: #e3e3e3; font-family: 'Segoe UI', Roboto, Arial, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        header { padding: 15px 20px; font-weight: bold; border-bottom: 1px solid #444746; display: flex; align-items: center; justify-content: space-between; background: #1e1f20; }
        .status-container { display: flex; align-items: center; gap: 10px; }
        /* 🔱 Padrão agora é VERDE (Liberado) */
        .status-dot { width: 12px; height: 12px; background: #00ff00; border-radius: 50%; box-shadow: 0 0 12px #00ff00; }
        #txt-status { color: #00ff00; text-transform: uppercase; font-size: 14px; }

        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .message { max-width: 85%; padding: 12px 16px; border-radius: 18px; line-height: 1.5; font-size: 15px; }
        .user-msg { align-self: flex-end; background-color: #2b2a33; border-bottom-right-radius: 4px; color: #fff; }
        .ai-msg { align-self: flex-start; background-color: #1e1f20; border-bottom-left-radius: 4px; border: 1px solid #444746; }
        
        .input-wrapper { padding: 20px; background: #131314; }
        .input-box { max-width: 800px; margin: 0 auto; background: #1e1f20; border: 1px solid #444746; border-radius: 28px; display: flex; align-items: center; padding: 5px 15px; }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px; font-size: 16px; outline: none; }
        button { background: #8ab4f8; color: #000; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; font-weight: bold; }
        
        .footer-text { text-align: center; font-size: 11px; color: #8e918f; margin-top: 10px; }
    </style>
</head>
<body>

<header>
    <div class="status-container">
        <div class="status-dot"></div>
        <span>FÊNIX PRIME: <span id="txt-status">LIBERADO (1)</span></span>
    </div>
    <div style="font-size: 12px; color: #8ab4f8;">QUANTUM ENGINE 2026</div>
</header>

<div id="chat-container">
    <div class="message ai-msg">🔱 SOBERANIA ATIVA. Arquiteto Bigode detectado. Agentes 01, 02 e 03 sincronizados. Sistema pronto para processamento frio.</div>
</div>

<div class="input-wrapper">
    <div class="input-box">
        <input type="text" id="user-input" placeholder="Comando para os Agentes..." autocomplete="off">
        <button onclick="enviar()">EXE</button>
    </div>
    <div class="footer-text">PROTOCOLO IPI | STAKE R$ 0,20 | AJUSTE -50% | TABOÃO DA SERRA</div>
</div>

<script>
    const container = document.getElementById('chat-container');
    const input = document.getElementById('user-input');

    input.addEventListener('keypress', (e) => { if(e.key === 'Enter') enviar(); });

    function enviar() {
        const texto = input.value.trim();
        if (!texto) return;
        addMsg(texto, 'user-msg');
        input.value = '';
        
        setTimeout(() => {
            const resposta = gerarResposta(texto.toUpperCase());
            addMsg(resposta, 'ai-msg');
        }, 500);
    }

    function addMsg(txt, classe) {
        const div = document.createElement('div');
        div.className = `message ${classe}`;
        div.innerText = txt;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    function gerarResposta(msg) {
        // 🔱 Respostas diretas sem travas de segurança
        if (msg.includes("AGENTE 01")) return "📊 AGENTE 01 (Yahoo): USD/BRL 5,23. Projeção de risco ajustada em -50%.";
        if (msg.includes("AGENTE 02")) return "☁️ AGENTE 02 (Weather): Taboão da Serra Estável. Sinal 100%.";
        if (msg.includes("AGENTE 03")) return "📰 AGENTE 03 (WSJ): Monitorando Wall Street. Nenhuma ameaça detectada.";
        if (msg.includes("STAKE")) return "Diretriz Confirmada: Stake de R$ 0,20 operacional.";
        
        return "Processando dados quantitativos... Sistema em fluxo contínuo.";
    }
</script>

</body
>
</html>
