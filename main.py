<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fênix Prime - Chat IA</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #131314; color: #e3e3e3; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        
        /* Header estilo Moderno */
        header { padding: 15px 20px; font-weight: 500; border-bottom: 1px solid #444746; display: flex; align-items: center; gap: 10px; }
        .status-dot { width: 10px; height: 10px; background: #00ff00; border-radius: 50%; box-shadow: 0 0 5px #00ff00; }

        /* Área de Mensagens */
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; scroll-behavior: smooth; }
        
        .message { max-width: 85%; padding: 12px 16px; border-radius: 18px; line-height: 1.5; font-size: 15px; }
        .user-msg { align-self: flex-end; background-color: #2b2a33; border-bottom-right-radius: 4px; color: #fff; }
        .ai-msg { align-self: flex-start; background-color: #1e1f20; border-bottom-left-radius: 4px; border: 1px solid #444746; }

        /* Campo de Input estilo ChatGPT/Gemini */
        .input-wrapper { padding: 20px; max-width: 800px; width: 100%; margin: 0 auto; position: relative; }
        .input-box { background: #1e1f20; border: 1px solid #444746; border-radius: 28px; display: flex; align-items: center; padding: 5px 15px; transition: 0.2s; }
        .input-box:focus-within { border-color: #8ab4f8; }
        
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px; font-size: 16px; outline: none; }
        button { background: #8ab4f8; color: #000; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; font-weight: bold; }

        .footer-text { text-align: center; font-size: 11px; color: #8e918f; margin-top: 10px; }
    </style>
</head>
<body>

<header>
    <div class="status-dot"></div>
    FÊNIX PRIME - METIS-BOND 3.0
</header>

<div id="chat-container">
    <div class="message ai-msg">Olá, Bigode. A interface 3.0 está ativa. Os 17 agentes estão em prontidão no servidor blindado. O que vamos operar hoje?</div>
</div>

<div class="input-wrapper">
    <div class="input-box">
        <input type="text" id="user-input" placeholder="Pergunte à Maiara..." autocomplete="off">
        <button onclick="enviar()">↑</button>
    </div>
    <div class="footer-text">Padrão Ouro: Stake R$ 0,20 | Ajuste -50% | Sistema Blindado</div>
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

        // Simulação da Resposta da Maiara
        setTimeout(() => {
            const resposta = gerarResposta(texto.toLowerCase());
            addMsg(resposta, 'ai-msg');
        }, 600);
    }

    function addMsg(txt, classe) {
        const div = document.createElement('div');
        div.className = `message ${classe}`;
        div.innerText = txt;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    function gerarResposta(msg) {
        if (msg.includes("status")) return "Sincronização 100%. LIBERADO(100%). Todos os 17 agentes estão operantes no back-end.";
        if (msg.includes("stake")) return "Padrão Ouro confirmado: Stake de R$ 0,20 por entrada conforme sua diretriz.";
        if (msg.includes("risco")) return "Análise IPI: Risco Médio. Decisão sugerida: ENTRA (com proteção de -50%).";
        return "Processando sua solicitação via Memória Quântica... Analisando variáveis para garantir o Padrão Ouro.";
    }
</script>

</
body>
</html>
