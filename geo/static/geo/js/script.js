function lerJson(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        return null;
    }
    return JSON.parse(elemento.textContent);
}

function aplicarPreferencias() {
    const tamanhoTexto = localStorage.getItem("geo_tamanho_texto");
    const contraste = localStorage.getItem("geo_alto_contraste");
    const reduzir = localStorage.getItem("geo_reduzir_estimulos");

    document.body.classList.remove("texto-grande", "texto-maior", "alto-contraste", "reduzir-estimulos");

    if (tamanhoTexto === "grande") {
        document.body.classList.add("texto-grande");
    }

    if (tamanhoTexto === "maior") {
        document.body.classList.add("texto-maior");
    }

    if (contraste === "sim") {
        document.body.classList.add("alto-contraste");
    }

    if (reduzir === "sim") {
        document.body.classList.add("reduzir-estimulos");
    }
}

function configurarAcessibilidade() {
    const aumentar = document.getElementById("aumentarTexto");
    const diminuir = document.getElementById("diminuirTexto");
    const contraste = document.getElementById("altoContraste");
    const reduzir = document.getElementById("reduzirEstimulos");

    if (aumentar) {
        aumentar.addEventListener("click", function () {
            const atual = localStorage.getItem("geo_tamanho_texto");
            localStorage.setItem("geo_tamanho_texto", atual === "grande" ? "maior" : "grande");
            aplicarPreferencias();
        });
    }

    if (diminuir) {
        diminuir.addEventListener("click", function () {
            localStorage.removeItem("geo_tamanho_texto");
            aplicarPreferencias();
        });
    }

    if (contraste) {
        contraste.addEventListener("click", function () {
            const ativo = localStorage.getItem("geo_alto_contraste") === "sim";
            localStorage.setItem("geo_alto_contraste", ativo ? "nao" : "sim");
            aplicarPreferencias();
        });
    }

    if (reduzir) {
        reduzir.addEventListener("click", function () {
            const ativo = localStorage.getItem("geo_reduzir_estimulos") === "sim";
            localStorage.setItem("geo_reduzir_estimulos", ativo ? "nao" : "sim");
            aplicarPreferencias();
        });
    }
}

function chaveAula(tema, aula) {
    return "geo_aula_" + tema + "_" + aula;
}

function configurarAula() {
    const aula = document.querySelector(".aula");
    const botao = document.getElementById("marcarAula");
    const status = document.getElementById("statusAula");

    if (!aula || !botao || !status) {
        return;
    }

    const tema = aula.dataset.tema;
    const numero = aula.dataset.aula;
    const chave = chaveAula(tema, numero);

    function atualizarStatus() {
        if (localStorage.getItem(chave) === "concluida") {
            status.textContent = "Aula concluída ✓";
            botao.textContent = "Aula concluída";
        }
    }

    botao.addEventListener("click", function () {
        localStorage.setItem(chave, "concluida");
        localStorage.setItem("geo_ultima_aula", JSON.stringify({ tema: tema, aula: numero }));
        atualizarStatus();
    });

    atualizarStatus();
}

function configurarBarraLeitura() {
    const barra = document.getElementById("barraLeitura");
    const aula = document.querySelector(".aula-rolagem");

    if (!barra || !aula) {
        return;
    }

    function atualizar() {
        const documento = document.documentElement;
        const alturaRolavel = documento.scrollHeight - window.innerHeight;
        const progresso = alturaRolavel > 0 ? (window.scrollY / alturaRolavel) * 100 : 0;
        barra.style.width = Math.min(100, Math.max(0, progresso)) + "%";
    }

    atualizar();
    window.addEventListener("scroll", atualizar, { passive: true });
    window.addEventListener("resize", atualizar);
}

function configurarAparecimento() {
    const elementos = document.querySelectorAll(".aparecer");

    if (!elementos.length) {
        return;
    }

    if (document.body.classList.contains("reduzir-estimulos") || !("IntersectionObserver" in window)) {
        elementos.forEach(function (elemento) {
            elemento.classList.add("visivel");
        });
        return;
    }

    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                entrada.target.classList.add("visivel");
                observador.unobserve(entrada.target);
            }
        });
    }, { threshold: 0.14 });

    elementos.forEach(function (elemento) {
        observador.observe(elemento);
    });
}

function configurarRevelarExplicacao() {
    document.querySelectorAll(".revelar-btn").forEach(function (botao) {
        botao.addEventListener("click", function () {
            const conteudo = botao.parentElement.querySelector(".revelar-conteudo");
            if (!conteudo) {
                return;
            }
            const escondido = conteudo.hasAttribute("hidden");
            if (escondido) {
                conteudo.removeAttribute("hidden");
                botao.setAttribute("aria-expanded", "true");
                botao.textContent = "Ocultar explicação";
            } else {
                conteudo.setAttribute("hidden", "");
                botao.setAttribute("aria-expanded", "false");
                botao.textContent = "Mostrar explicação";
            }
        });
    });
}

function configurarPerguntasRapidas() {
    document.querySelectorAll(".pergunta-rapida").forEach(function (area) {
        const feedback = area.querySelector(".pergunta-feedback");
        area.querySelectorAll(".pergunta-btn").forEach(function (botao) {
            botao.addEventListener("click", function () {
                const correta = botao.dataset.correta === "true";
                const classe = correta ? "alert-success" : "alert-warning";
                const prefixo = correta ? botao.textContent.trim() + " ✓" : "Quase. ";
                feedback.innerHTML = '<div class="alert ' + classe + '"><strong>' + prefixo + '</strong> ' + feedback.dataset.explicacao + "</div>";
            });
        });
    });
}

function configurarMarcadoresImagem() {
    document.querySelectorAll(".marcador-imagem").forEach(function (botao) {
        botao.addEventListener("click", function () {
            const secao = botao.closest(".secao-aula");
            const feedback = secao ? secao.querySelector(".marcador-feedback") : null;
            if (feedback) {
                feedback.textContent = botao.dataset.texto;
            }
        });
    });
}

function configurarZoomImagens() {
    const modal = document.getElementById("modalImagem");
    const imagem = document.getElementById("modalImagemArquivo");
    const fonte = document.getElementById("modalImagemFonte");

    if (!modal || !imagem || !fonte) {
        return;
    }

    modal.addEventListener("show.bs.modal", function (evento) {
        const botao = evento.relatedTarget;
        if (!botao) {
            return;
        }
        imagem.src = botao.dataset.src;
        imagem.alt = botao.dataset.alt;
        fonte.textContent = "Fonte: " + botao.dataset.fonte;
    });

    modal.addEventListener("hidden.bs.modal", function () {
        imagem.src = "";
        imagem.alt = "";
        fonte.textContent = "";
    });
}

function configurarAtividades() {
    document.querySelectorAll(".vf-btn").forEach(function (botao) {
        botao.addEventListener("click", function () {
            const item = botao.closest(".vf-item");
            const correto = item.dataset.resposta === botao.dataset.valor;
            const feedback = item.querySelector(".vf-feedback");
            const classe = correto ? "alert alert-success" : "alert alert-danger";
            const inicio = correto ? "Correto." : "Revise.";
            feedback.innerHTML = '<div class="' + classe + ' mb-0"><strong>' + inicio + '</strong> ' + item.dataset.explicacao + "</div>";
        });
    });

    document.querySelectorAll(".flashcard").forEach(function (card) {
        card.addEventListener("click", function () {
            const virado = card.classList.toggle("virado");
            card.textContent = virado ? card.dataset.verso : card.dataset.frente;
        });
    });
}

function calcularTema(tema) {
    let concluidas = 0;
    tema.aulas.forEach(function (aula) {
        if (localStorage.getItem(chaveAula(tema.slug, aula.numero)) === "concluida") {
            concluidas++;
        }
    });
    return Math.round((concluidas / tema.aulas.length) * 100);
}

function mostrarProgresso() {
    const area = document.getElementById("areaProgresso");
    const temas = lerJson("temas-data");

    if (!area || !temas) {
        return;
    }

    let html = "";
    let soma = 0;

    temas.forEach(function (tema) {
        const porcentagem = calcularTema(tema);
        soma += porcentagem;
        const quiz = localStorage.getItem("geo_quiz_" + tema.slug);
        const textoQuiz = quiz ? "Quiz: " + quiz : "Quiz ainda não registrado";
        const aulaUrl = "/aula/" + tema.slug + "/1/";

        html += `
            <article class="card mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between flex-wrap gap-2">
                        <h2 class="h5 mb-1">${tema.titulo}</h2>
                        <span>${porcentagem}% das aulas</span>
                    </div>
                    <div class="progress mt-2" role="progressbar" aria-label="Progresso em ${tema.titulo}" aria-valuenow="${porcentagem}" aria-valuemin="0" aria-valuemax="100">
                        <div class="progress-bar bg-success" style="width: ${porcentagem}%">${porcentagem}%</div>
                    </div>
                    <p class="small text-muted mt-2 mb-2">${textoQuiz}</p>
                    <a class="btn btn-sm btn-outline-success" href="${aulaUrl}">Estudar tema</a>
                </div>
            </article>
        `;
    });

    const geral = Math.round(soma / temas.length);
    area.innerHTML = `
        <div class="alert alert-success">Progresso geral: ${geral}%.</div>
        <div class="progress mb-4" role="progressbar" aria-label="Progresso geral" aria-valuenow="${geral}" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar bg-success" style="width: ${geral}%">${geral}%</div>
        </div>
        ${html}
    `;
}

function mostrarContinuar() {
    const area = document.getElementById("continuarArea");
    const temas = lerJson("temas-data");
    const ultima = localStorage.getItem("geo_ultima_aula");

    if (!area || !temas || !ultima) {
        return;
    }

    const dados = JSON.parse(ultima);
    const tema = temas.find(function (item) {
        return item.slug === dados.tema;
    });

    if (!tema) {
        return;
    }

    area.innerHTML = `
        <div class="alert alert-success mt-3">
            <strong>Continue de onde parou:</strong>
            <a href="/aula/${dados.tema}/${dados.aula}/">Aula ${dados.aula} de ${tema.titulo}</a>
        </div>
    `;
}

document.addEventListener("DOMContentLoaded", function () {
    aplicarPreferencias();
    configurarAcessibilidade();
    configurarAula();
    configurarBarraLeitura();
    configurarAparecimento();
    configurarRevelarExplicacao();
    configurarPerguntasRapidas();
    configurarMarcadoresImagem();
    configurarZoomImagens();
    configurarAtividades();
    mostrarProgresso();
    mostrarContinuar();
});
