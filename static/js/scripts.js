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
    const tirarFoto = document.getElementById("tirarFoto");
    const inputImagem = document.getElementById("inputImagem");

    let stream = null;

    // Função para ativar a câmera
    async function ativarCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: { ideal: "environment" } } // Usa a câmera traseira se disponível
            });
            video.srcObject = stream;
            video.style.display = "block";
            tirarFoto.textContent = "Capturar Foto";
        } catch (err) {
            console.error("Erro ao acessar a câmera: ", err);
            alert("Erro ao acessar a câmera. Verifique as permissões do navegador.");
        }
    }

    // Captura a foto e adiciona ao input de arquivo
    function capturarFoto() {
        if (stream) {
            canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
            video.style.display = "none";

            // Parar a câmera
            stream.getTracks().forEach(track => track.stop());
            stream = null;
            tirarFoto.textContent = "Tirar Foto";

            // Converte a imagem para um arquivo e adiciona ao input de imagem
            canvas.toBlob(function (blob) {
                const file = new File([blob], "captura.jpg", { type: "image/jpeg" });

                let dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                inputImagem.files = dataTransfer.files;
            }, "image/jpeg");
        }
    }

    // Adiciona evento ao botão "Tirar Foto"
    tirarFoto.addEventListener("click", function () {
        if (!stream) {
            ativarCamera();
        } else {
            capturarFoto();
        }
    });
});
