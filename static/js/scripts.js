function togglePopup() {
  var popup = document.getElementById('popup');
  var isHidden = popup.getAttribute('aria-hidden') === 'true';
  popup.setAttribute('aria-hidden', !isHidden);
  
  if (!isHidden) {
    popup.focus(); // Focar no popup para facilitar a navegação com teclado
  }
}

document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ativarCameraBtn = document.getElementById("ativarCamera");
    const capturarFotoBtn = document.getElementById("capturarFoto");
    const cameraSelect = document.getElementById("cameraSelect");
    const imagemCapturada = document.getElementById("imagemCapturada");
    const imagemPreview = document.getElementById("imagemPreview");
    let stream = null;

    ativarCameraBtn.addEventListener("click", function () {
        const facingMode = cameraSelect.value; // "user" = frontal, "environment" = traseira

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("Erro: Seu navegador não suporta acesso à câmera.");
            return;
        }

        navigator.mediaDevices.getUserMedia({ video: { facingMode: facingMode } })
            .then(function (mediaStream) {
                stream = mediaStream;
                video.srcObject = stream;
                video.style.display = "block";
                capturarFotoBtn.style.display = "block";
            })
            .catch(function (err) {
                console.error("Erro ao acessar a câmera:", err);
                alert("Erro ao acessar a câmera: " + err.message);
            });
    });

    capturarFotoBtn.addEventListener("click", function () {
        if (!stream) {
            alert("Erro: A câmera não está ativa.");
            return;
        }

        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, 320, 240);

        const imageData = canvas.toDataURL("image/png");
        imagemCapturada.value = imageData; // Armazena a imagem no input oculto para ser enviada
        imagemPreview.src = imageData;
        imagemPreview.style.display = "block";

        // Parar a câmera após capturar a foto
        stream.getTracks().forEach(track => track.stop());
        video.style.display = "none";
        capturarFotoBtn.style.display = "none";
    });
});
