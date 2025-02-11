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
    const capturarFoto = document.getElementById("capturarFoto");
    const inputImagem = document.getElementById("id_imagem");

    if (capturarFoto) {
        capturarFoto.addEventListener("click", function () {
            // Exibir a câmera
            video.style.display = "block";
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    video.srcObject = stream;
                })
                .catch(function (err) {
                    console.error("Erro ao acessar a câmera: ", err);
                    alert("Erro ao acessar a câmera. Verifique as permissões do navegador.");
                });
        });

        video.addEventListener("click", function () {
            // Capturar a imagem do vídeo
            canvas.style.display = "block";
            canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
            video.style.display = "none";

            // Parar o stream da câmera
            video.srcObject.getTracks().forEach(track => track.stop());

            // Converter imagem em blob e definir no input de arquivo
            canvas.toBlob(function (blob) {
                const file = new File([blob], "captura.jpg", { type: "image/jpeg" });

                // Criar um objeto DataTransfer para definir a imagem capturada no campo de arquivo
                let dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                inputImagem.files = dataTransfer.files;
            }, "image/jpeg");
        });
    }
});
