let perguntaAtual = 0;
let acertos = 0;
let respondeu = false;

function perguntasDoQuiz() {
    return JSON.parse(document.getElementById("perguntas-data").textContent);
}

function textoAlternativa(alternativa) {
    return typeof alternativa === "string" ? alternativa : alternativa.texto;
}

function alternativaCorreta(pergunta, alternativa, indice) {
    if (typeof alternativa === "object" && alternativa !== null && "correta" in alternativa) {
        return alternativa.correta === true;
    }
    return indice === pergunta.correta;
}

function mostrarQuiz() {
    const area = document.getElementById("areaQuiz");
    if (!area) {
        return;
    }

    const perguntas = perguntasDoQuiz();
    const pergunta = perguntas[perguntaAtual];
    const progresso = Math.round(((perguntaAtual + 1) / perguntas.length) * 100);
    let alternativas = "";

    pergunta.alternativas.forEach(function (alternativa, indice) {
        alternativas += `
            <button class="btn btn-outline-success alternativa" type="button" data-indice="${indice}" aria-pressed="false">
                ${textoAlternativa(alternativa)}
            </button>
        `;
    });

    area.innerHTML = `
        <p>Questão ${perguntaAtual + 1} de ${perguntas.length}</p>
        <div class="progress mb-3" role="progressbar" aria-label="Progresso do quiz" aria-valuenow="${progresso}" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar bg-success" style="width: ${progresso}%">${progresso}%</div>
        </div>
        <section class="card">
            <div class="card-body">
                <h2 class="h4">${pergunta.pergunta}</h2>
                <div id="alternativas" class="mt-3">${alternativas}</div>
                <button class="btn btn-success mt-2" id="responderQuiz" type="button">Responder</button>
                <div id="resultadoQuiz" class="mt-3" role="status"></div>
            </div>
        </section>
    `;

    document.querySelectorAll(".alternativa").forEach(function (botao) {
        botao.addEventListener("click", function () {
            document.querySelectorAll(".alternativa").forEach(function (item) {
                item.setAttribute("aria-pressed", "false");
                item.classList.remove("active");
            });
            botao.setAttribute("aria-pressed", "true");
            botao.classList.add("active");
        });
    });

    document.getElementById("responderQuiz").addEventListener("click", responderQuiz);
}

function responderQuiz() {
    if (respondeu) {
        return;
    }

    const perguntas = perguntasDoQuiz();
    const pergunta = perguntas[perguntaAtual];
    const escolhida = document.querySelector('.alternativa[aria-pressed="true"]');
    const resultado = document.getElementById("resultadoQuiz");

    if (!escolhida) {
        resultado.innerHTML = '<div class="alert alert-warning">Escolha uma alternativa antes de responder.</div>';
        return;
    }

    respondeu = true;
    const indice = Number(escolhida.dataset.indice);
    const acertou = alternativaCorreta(pergunta, pergunta.alternativas[indice], indice);

    if (acertou) {
        acertos++;
    }

    resultado.innerHTML = `
        <div class="alert ${acertou ? "alert-success" : "alert-danger"}">
            <strong>${acertou ? "Correto." : "Resposta incorreta."}</strong> ${pergunta.explicacao}
        </div>
        <button class="btn btn-outline-success" id="avancarQuiz" type="button">
            ${perguntaAtual < perguntas.length - 1 ? "Próxima pergunta" : "Ver resultado"}
        </button>
    `;

    document.getElementById("avancarQuiz").addEventListener("click", avancarQuiz);
}

function avancarQuiz() {
    const perguntas = perguntasDoQuiz();
    if (perguntaAtual < perguntas.length - 1) {
        perguntaAtual++;
        respondeu = false;
        mostrarQuiz();
        return;
    }
    finalizarQuiz();
}

function finalizarQuiz() {
    const area = document.getElementById("areaQuiz");
    const perguntas = perguntasDoQuiz();
    const tema = area.dataset.tema;
    const temaTitulo = area.dataset.temaTitulo;
    const temaUrl = area.dataset.temaUrl;
    const progressoUrl = area.dataset.progressoUrl;

    localStorage.setItem("geo_quiz_" + tema, acertos + " de " + perguntas.length + " acertos");

    area.innerHTML = `
        <section class="card">
            <div class="card-body">
                <h2>Resultado do quiz</h2>
                <p class="lead">Você acertou ${acertos} de ${perguntas.length} perguntas sobre ${temaTitulo}.</p>
                <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-success" id="refazerQuiz" type="button">Refazer quiz</button>
                    <a class="btn btn-outline-success" href="${temaUrl}">Voltar ao tema</a>
                    <a class="btn btn-outline-secondary" href="${progressoUrl}">Ver progresso</a>
                </div>
            </div>
        </section>
    `;

    document.getElementById("refazerQuiz").addEventListener("click", function () {
        perguntaAtual = 0;
        acertos = 0;
        respondeu = false;
        mostrarQuiz();
    });
}

document.addEventListener("DOMContentLoaded", mostrarQuiz);
