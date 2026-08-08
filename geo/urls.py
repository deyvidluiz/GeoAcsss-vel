from django.urls import path

from . import views

app_name = "geo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ano/<int:ano>/", views.ano, name="ano"),
    path("tema/<slug:tema_slug>/", views.tema, name="tema"),
    path("aula/<slug:tema_slug>/<int:numero>/", views.aula, name="aula"),
    path("quiz/<slug:tema_slug>/", views.quiz, name="quiz"),
    path("atividade/<slug:tema_slug>/", views.atividade, name="atividade"),
    path("progresso/", views.progresso, name="progresso"),
    path("sobre/", views.sobre, name="sobre"),
]
