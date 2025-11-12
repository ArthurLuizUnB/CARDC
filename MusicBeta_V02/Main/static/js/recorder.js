// MusicBeta_V02/Main/static/js/recorder.js

// Espera o DOM estar pronto
document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Pega os elementos do HTML
    const startRecordBtn = document.getElementById("startRecordBtn");
    const stopRecordBtn = document.getElementById("stopRecordBtn");
    const videoPreview = document.getElementById("videoPreview"); // <video> para o preview
    const videoUploadInput = document.getElementById("video_upload"); // <input type="file">

    if (!startRecordBtn) {
        // Se não encontrar os botões (ex: em outra página), não faz nada
        return;
    }

    let mediaRecorder; // O objeto que realmente grava
    let recordedChunks = []; // Um array para guardar os "pedaços" do vídeo

    // 2. Ação do Botão "Gravar"
    startRecordBtn.addEventListener("click", async () => {
        try {
            // Pedir permissão para câmera e microfone
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: true, 
                audio: true 
            });
            
            // Mostrar o preview da câmera no elemento <video>
            videoPreview.srcObject = stream;
            videoPreview.style.display = "block"; // Mostra o player
            
            // Inicia o gravador
            mediaRecorder = new MediaRecorder(stream);
            
            // O que fazer quando o gravador parar
            mediaRecorder.onstop = () => {
                // 1. Cria um "Blob" (um arquivo "virtual") com os pedaços gravados
                const videoBlob = new Blob(recordedChunks, { type: "video/webm" });

                // 2. Cria um objeto "File" a partir do Blob
                const recordedFile = new File([videoBlob], "gravacao.webm", {
                    type: "video/webm",
                    lastModified: new Date().getTime(),
                });

                // 3. ESSENCIAL: Coloca o arquivo gravado dentro do input "video_upload"
                // Para isso, usamos um DataTransfer
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(recordedFile);
                videoUploadInput.files = dataTransfer.files;

                // Limpa os pedaços e o stream
                recordedChunks = [];
                stream.getTracks().forEach(track => track.stop()); // Desliga a câmera
                videoPreview.srcObject = null;
                
                // Atualiza a interface
                startRecordBtn.classList.remove("is-recording");
                startRecordBtn.disabled = false;
                stopRecordBtn.disabled = true;
                alert("Gravação finalizada! Clique em 'Salvar' no final do formulário para enviar.");
            };

            // O que fazer quando um "pedaço" de vídeo estiver pronto
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            // Inicia a gravação e atualiza a interface
            mediaRecorder.start();
            startRecordBtn.classList.add("is-recording");
            startRecordBtn.disabled = true;
            stopRecordBtn.disabled = false;

        } catch (error) {
            console.error("Erro ao acessar a câmera:", error);
            alert("Não foi possível acessar sua câmera. Verifique as permissões do navegador.");
        }
    });

    // 3. Ação do Botão "Parar"
    stopRecordBtn.addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
    });
});