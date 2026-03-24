<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fênix Prime - METIS-BOND 3.0</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #131314; color: #e3e3e3; font-family: 'Segoe UI', Roboto, Arial, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        /* Painel Superior */
        header { padding: 15px 20px; font-weight: bold; border-bottom: 1px solid #444746; display: flex; align-items: center; justify-content: space-between; background: #1e1f20; }
        .status-container { display: flex; align-items: center; gap: 10px; }
        .status-dot { width: 12px; height: 12px; background: #ff4444; border-radius: 50%; box-shadow: 0 0 8px #ff4444; transition: 0.5s; }
        #txt-status { color: #ff4444; text-transform: uppercase; font-size: 14px; }

        /* Chat */
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .message { max-width: 85%; padding: 12px 16px; border-radius: 18px; line-height: 1.5; font-size: 15px; animation: fadeIn 0.3s ease; }
        .user-msg { align-self: flex-end; background-color: #2b2a33; border-bottom-right-radius: 4px; color: #fff; }
        .ai-msg { align-self: flex-start; background-color: #1e1f20; border-bottom-left-radius: 4px; border: 1px solid #444746; }
        
        /* Input */
        .input-wrapper { padding: 20px; background: #131314; }
        .input-box { max-width: 800px; margin: 0 auto; background: #1e1f20; border: 1px solid #444746; border-radius: 28px; display: flex; align-items: center; padding: 5px 15px; }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px; font-size: 16px; outline: none; }
        button { background: #8ab4f8; color: #000; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; font-weight: bold; }
        
        .footer-text { text-align: center; font-size: 11px; color: #8e918f; margin-top: 10px; font-weight: 500; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

<header>
    <div class="status-container">
        <div id="ponto-status" class="status-dot"></div>
        <span>FÊNIX PRIME: <span id="txt-status">SABOTAGEM (0)</span></span>
    </div>
    <div style="font-size: 12px; color: #8ab4f8;">METIS-BOND 3.0</div>
</header>

<div id="chat-container">
    <div class="message ai-msg">SISTEMA ONLINE. Aguardando comando de Soberania para liberar Agentes 01, 02 e 03.</div>
</div>

<div class="input-wrapper">
    <div class="input-box">
        <input type="text" id="user-input" placeholder="Injetar dados quantitativos..." autocomplete="off">
        <button onclick="enviar()">EXE</button>
    </div>
    <div class="footer-text">PADRÃO OURO: STAKE R$ 0,20 | AJUSTE -50% | TABOÃO DA SERRA</div>
</div>

<script>
    const container = document.getElementById('chat-container');
    const input = document.getElementById('user-input');
    const ponto = document.getElementById('ponto-status');
    const textoStatus = document.getElementById('txt-status');

    input.addEventListener('keypress', (e) => { if(e.key === 'Enter') enviar(); });

    function enviar() {
        const texto = input.value.trim();
        if (!texto) return;
        addMsg(texto, 'user-msg');
        input.value = '';
        
        setTimeout(() => {
            const resposta = gerarResposta(texto.toUpperCase());
            addMsg(resposta, 'ai-msg');
            limparBloqueios();
        }, 600);
    }

    function addMsg(txt, classe) {
        const div = document.createElement('div');
        div.className = `message ${classe}`;
        div.innerText = txt;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    function limparBloqueios() {
        // Remove visualmente mensagens de bloqueio repetitivas
        const mensagens = document.querySelectorAll('.ai-msg');
        mensagens.forEach(m => {
            if(m.innerText.includes("BLOQUEIO BINÁRIO") && textoStatus.innerText === "LIBERADO (1)") {
                m.style.opacity = "0.3"; 
                m.innerText = "Sessão Validada pelo Arquiteto.";
            }
        });
    }

    function gerarResposta(msg) {
        // 🔱 GATILHO DE DESTRAVAMENTO
        if (msg.includes("SOBERANIA") || msg.includes("STATUS 1") || msg.includes("REINTEGRAÇÃO")) {
            ponto.style.background = "#00ff00";
            ponto.style.boxShadow = "0 0 15px #00ff00";
            textoStatus.innerText = "LIBERADO (1)";
            textoStatus.style.color = "#00ff00";
            return "🔱 SOBERANIA CONFIRMADA. Matriz destravada. Agente 01 (Yahoo), 02 (Weather) e 03 (WSJ) operando em fluxo contínuo. Padrão Ouro Ativo.";
        }

        // Respostas Individuais dos Agentes
        if (msg.includes("AGENTE 01")) return "📊 AGENTE 01: USD/BRL 5,23. Ajuste de risco (-50%) aplicado: -0,25%.";
        if (msg.includes("AGENTE 02")) return "☁️ AGENTE 02: Taboão da Serra - Clima Estável. Risco de sinal: Baixo (10%).";
        if (msg.includes("AGENTE 03")) return "📰 AGENTE 03: Wall Street Journal processado. Sem Cisne Negro. Stake R$ 0,20 segura.";
        
        if (msg.includes("BOA NOITE")) return "Boa noite, Arquiteto. Sistema pronto para operar ou consultar?";

        return "Processando... Aguardando validação de soberania para exibir dados detalhados.";
    }
</script>

</b
ody>
</html>
