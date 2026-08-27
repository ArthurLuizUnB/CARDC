// MusicBeta_V02/Main/static/js/recorder.js
// Gerencia as abas de mídia (vídeo/áudio) e a gravação pelo microfone.

document.addEventListener("DOMContentLoaded", () => {

    // ===== ALTERNÂNCIA DE ABAS =====
    window.alternarAba = function(tipo) {
        const painelVideo = document.getElementById("painel-video");
        const painelAudio = document.getElementById("painel-audio");
        const abaVideo    = document.getElementById("aba-video");
        const abaAudio    = document.getElementById("aba-audio");
        const tipoMidia   = document.getElementById("tipo_midia");

        if (!painelVideo) return;

        if (tipo === "audio") {
            painelVideo.classList.add("oculto");
            painelAudio.classList.remove("oculto");
            abaVideo.classList.remove("ativa");
            abaAudio.classList.add("ativa");
            abaVideo.setAttribute("aria-selected", "false");
            abaAudio.setAttribute("aria-selected", "true");
            tipoMidia.value = "audio";
        } else {
            painelAudio.classList.add("oculto");
            painelVideo.classList.remove("oculto");
            abaAudio.classList.remove("ativa");
            abaVideo.classList.add("ativa");
            abaAudio.setAttribute("aria-selected", "false");
            abaVideo.setAttribute("aria-selected", "true");
            tipoMidia.value = "video";
        }
    };

    // ===== EXIBIR NOME DO ARQUIVO SELECIONADO =====
    const videoInput = document.getElementById("video_upload");
    const audioInput = document.getElementById("audio_upload");

    if (videoInput) {
        videoInput.addEventListener("change", () => {
            const nome = videoInput.files[0]?.name || "";
            document.getElementById("video-nome-arquivo").textContent =
                nome ? "📎 " + nome : "";
        });
    }

    if (audioInput) {
        audioInput.addEventListener("change", () => {
            const nome = audioInput.files[0]?.name || "";
            document.getElementById("audio-nome-arquivo").textContent =
                nome ? "📎 " + nome : "";
        });
    }

    // ===== GRAVAÇÃO DE ÁUDIO PELO MICROFONE =====
    const btnGravar = document.getElementById("btnGravarAudio");
    const btnParar  = document.getElementById("btnPararAudio");
    const status    = document.getElementById("statusGravacao");

    if (!btnGravar) return;

    let mediaRecorder;
    let chunks = [];

    btnGravar.addEventListener("click", async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            mediaRecorder = new MediaRecorder(stream);
            chunks = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) chunks.push(e.data);
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: "audio/webm" });
                const file = new File([blob], "gravacao.webm", {
                    type: "audio/webm",
                    lastModified: Date.now(),
                });

                const dt = new DataTransfer();
                dt.items.add(file);
                audioInput.files = dt.files;

                stream.getTracks().forEach(t => t.stop());

                btnGravar.disabled = false;
                btnParar.disabled  = true;
                btnGravar.classList.remove("is-recording");
                status.textContent = "✅ Gravação pronta! Clique em 'Salvar' para enviar.";
                document.getElementById("audio-nome-arquivo").textContent = "📎 gravacao.webm";
            };

            mediaRecorder.start();
            btnGravar.disabled = true;
            btnParar.disabled  = false;
            btnGravar.classList.add("is-recording");
            status.textContent = "🔴 Gravando...";

        } catch (err) {
            console.error("Erro ao acessar o microfone:", err);
            status.textContent = "❌ Não foi possível acessar o microfone. Verifique as permissões.";
        }
    });

    btnParar.addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
    });
});