import random

from django.http import Http404
from django.shortcuts import render

from .dados import ANOS, ATIVIDADES, CURIOSIDADES, PERGUNTAS, TEMAS, resumo_temas_para_navegador, temas_por_ano


def inicio(request):
    anos = [
        {**dados, "numero": numero, "temas": temas_por_ano(numero)}
        for numero, dados in ANOS.items()
    ]
    return render(request, "geo/inicio.html", {
        "anos": anos,
        "curiosidade": random.choice(CURIOSIDADES),
        "temas_json": resumo_temas_para_navegador(),
    })


def ano(request, ano):
    if ano not in ANOS:
        raise Http404("Ano não encontrado")
    return render(request, "geo/ano.html", {
        "ano_numero": ano,
        "ano": ANOS[ano],
        "temas": temas_por_ano(ano),
    })


def tema(request, tema_slug):
    tema_atual = TEMAS.get(tema_slug)
    if not tema_atual:
        raise Http404("Tema não encontrado")
    return render(request, "geo/tema.html", {
        "tema": tema_atual,
        "ano": ANOS[tema_atual["ano"]],
    })


def aula(request, tema_slug, numero):
    tema_atual = TEMAS.get(tema_slug)
    if not tema_atual or numero < 1 or numero > len(tema_atual["aulas"]):
        raise Http404("Aula não encontrada")

    aula_atual = tema_atual["aulas"][numero - 1]
    proxima = numero + 1 if numero < len(tema_atual["aulas"]) else None
    anterior = numero - 1 if numero > 1 else None

    return render(request, "geo/aula.html", {
        "tema": tema_atual,
        "ano": ANOS[tema_atual["ano"]],
        "aula": aula_atual,
        "proxima": proxima,
        "anterior": anterior,
    })


def quiz(request, tema_slug):
    tema_atual = TEMAS.get(tema_slug)
    if not tema_atual:
        raise Http404("Tema não encontrado")
    return render(request, "geo/quiz.html", {
        "tema": tema_atual,
        "ano": ANOS[tema_atual["ano"]],
        "perguntas_json": PERGUNTAS[tema_slug],
    })


def atividade(request, tema_slug):
    tema_atual = TEMAS.get(tema_slug)
    if not tema_atual:
        raise Http404("Tema não encontrado")
    return render(request, "geo/atividade.html", {
        "tema": tema_atual,
        "ano": ANOS[tema_atual["ano"]],
        "atividade": ATIVIDADES[tema_slug],
    })


def progresso(request):
    return render(request, "geo/progresso.html", {
        "temas_json": resumo_temas_para_navegador(),
    })


def sobre(request):
    return render(request, "geo/sobre.html")
