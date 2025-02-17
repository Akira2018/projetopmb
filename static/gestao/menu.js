document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll(".nav-item");

    // Comportamento para hover
    navItems.forEach(item => {
        const dropdown = item.querySelector(".nav-dropdown");

        // Exibe o menu ao passar o mouse
        item.addEventListener("mouseenter", () => {
            if (dropdown) {
                dropdown.style.display = "block";
            }
        });

        // Oculta o menu ao sair do mouse
        item.addEventListener("mouseleave", () => {
            if (dropdown) {
                setTimeout(() => {
                    dropdown.style.display = "none";
                }, 300); // 300ms de delay
            }
        });

        // Alterna o menu ao clicar (para dispositivos móveis)
        item.addEventListener("click", () => {
            if (dropdown) {
                dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
            }
        });
    });
});
