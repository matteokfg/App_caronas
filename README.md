# UNISO Caronas #
Protótipo do UNISO Caronas do grupo do Projeto Integrador do 1º semestre de 2022, utilizando a biblioteca Django do Python.

## Explicação do Django Template Language (DTL) ##
Foi utilizado o framework Django (versão 3.2), um framework Python para desenvolvimento web que permite a construção de aplicações web de alto desempenho. Por conta disso, o projeto tem como linguagem de template baseada em texto, a própria linguagem do Django, o Django Template Language (DTL), que é responsável por criar páginas HTML em projetos com Django, fazendo com que os arquivos HTML deixem de ser apenas estáticos e tenham também partes dinâmicas.

Os principais termos em DTL utilizados no projeto foram:

- `{% extends 'arquivo.HTML' %}`: implica a utilização do “arquivo.html” como base, preenchendo apenas os blocos que estiverem dentro dos “blocks”.

- `{% block algum_nome %}`: início de um bloco HTML, que será inserido no seu respectivo "buraco" no “arquivo.html”.

- `{% endblock %}`: fecha o bloco atual de conteúdo HTML.

- `{% include '.../outro_arquivo.HTML' %}`: inclui onde estiverem as “tags HTML” presentes no “outro_arquivo.html”.

- `{% include 'outro_arquivo.html' with var=alguma_variavel %}`: inclui o “outro_arquivo.html”, onde estiver. E como o outro arquivo utiliza algumas informações, essas são passadas pelo “with”, sendo atribuídas a variável “var”.

- `{% if condicao %}`: o conteúdo em HTML apenas aparecerá se a condição for satisfeita.

- `{% else %}`: indica o que acontecerá se a condição não for satisfeita.

- `{% endif %}`: encerra o teste condicional.

- `{% item for lista %}`: recebe uma lista e faz um laço de repetição, passando para cada interação um item por vez da lista.

- `{% endfor %}`: encerra o laço de repetição.

- `{% load static %}`: carrega a pasta “static”, dentro dela tem a pasta “css”, com todos os arquivos CSS.

- `{% load crispy_forms_tags %}`: carrega as “tags/classes” a serem incluídas nos formulários automáticos. Classes vindas do bootstrap 4.

- `{% static 'uma_pasta/arquivo.extensão' %}`: faz link para o “arquivo.extensão” em  “uma_pasta” dentro da pasta “static”.

- `{% url 'nome_da_url_e_view' %}`: dentro do atributo “href” de uma “tag” <a>, fazendo conexão com outra tela do projeto. Quando clicado, vai no arquivo “app/urls.py”, procura o caminho com nome “nome_da_url_e_view”, a “path” definida com esse nome irá para a URL no navegador, e a “view” será chamada. Essa “view” está em “app/views.py”. Lá ela vai passar o arquivo HTML a ser renderizado e as variáveis, listas ou dicionários necessários para a renderização, dentro de um dicionário, comumente chamado de “context”.

- `{{ variavel }}`: o valor dessa variável será passado para ser renderizado.

- `{{ algum_formulario|crispy }}`: o formulário automático do Django, passado pelo “context”, como uma variável chamada “algum_formulario”, será renderizado, com as suas “tags” com classes do Bootstrap 4.
