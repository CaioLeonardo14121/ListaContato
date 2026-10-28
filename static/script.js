// SAUDAÇÃO AUTOMÁTICA
const saudacao = document.getElementById("saudacao");

if (saudacao) {
    const hora = new Date().getHours();

    if (hora >= 5 && hora < 12) {
        saudacao.textContent = "Bom dia! Seja bem-vindo(a).";
    } else if (hora >= 12 && hora < 18) {
        saudacao.textContent = "Boa tarde! Seja bem-vindo(a).";
    } else {
        saudacao.textContent = "Boa noite! Seja bem-vindo(a).";
    }
}

// MENU PARA CELULAR
const menuToggle = document.getElementById("menu-toggle");
const menu = document.getElementById("menu");

if (menuToggle && menu) {
    menuToggle.addEventListener("click", function () {
        const aberto = menu.classList.toggle("aberto");

        menuToggle.setAttribute("aria-expanded", aberto);
        menuToggle.setAttribute(
            "aria-label",
            aberto ? "Fechar menu" : "Abrir menu"
        );
    });

    menu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            menu.classList.remove("aberto");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Abrir menu");
        });
    });
}

// ALTERNAR TEMA
const botaoTema = document.getElementById("tema");

if (botaoTema) {
    botaoTema.addEventListener("click", function () {
        document.body.classList.toggle("modo-claro");

        const modoClaro = document.body.classList.contains("modo-claro");

        botaoTema.textContent = modoClaro ? "☾" : "☼";
        botaoTema.setAttribute(
            "aria-label",
            modoClaro ? "Ativar modo escuro" : "Ativar modo claro"
        );
    });
}

// ATUALIZAR ANO
const ano = document.getElementById("ano");

if (ano) {
    ano.textContent = new Date().getFullYear();
}