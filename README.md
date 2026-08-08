# GeoAcessível

Site educacional de Geografia para estudantes do Ensino Médio, com atenção à acessibilidade para estudantes com TEA.

## Tecnologias

- Python
- Django
- HTML, CSS e JavaScript puro
- Bootstrap via CDN
- SQLite

## Como executar

```bash
python3 manage.py migrate
python3 manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Estrutura principal

- `geo/dados.py`: temas, aulas, perguntas, atividades e curiosidades.
- `geo/views.py`: function-based views das páginas.
- `geo/urls.py`: URLs simples do site.
- `geo/templates/geo/`: templates HTML.
- `geo/static/geo/css/style.css`: visual e acessibilidade.
- `geo/static/geo/js/script.js`: preferências, atividades e progresso.
- `geo/static/geo/js/quiz.js`: funcionamento do quiz.

O progresso das aulas, resultado dos quizzes e preferências de acessibilidade ficam no `localStorage` do navegador.
# GeoAcsss-vel
