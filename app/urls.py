from django.urls import path
from . import views

# nos templates: em tags 'a', a atributo 'href', vai ter seu valor: '{% url 'nome_da_url' %}'
# quando o usuario clicar nesse link, a requisicao vai passar pelo Middleware, vai ir em unisocar/urls.py, e vai chegar aqui, procurando a url com o nome passado
# lista com urls dentro de 'app'
urlpatterns = [
    # path('endpoint', view.a_ser_chamada, name='nome_da_url')
    path('', views.inicio_index, name='index'),                                                     # url do inicio
    path('login', views.login_user, name='login'),                                                  # url do login
    path('logout', views.logout_user, name='logout'),                                               # url do logout

    path('cadastro', views.cadastro, name='cadastro'),                                              # url de cadastro do User
    path('cadastro/passageiro', views.cadastro_passageiro, name='cadastro_passageiro'),             # url de cadastro do passageiro
    path('cadastro/motorista', views.cadastro_motorista, name='cadastro_motorista'),                # url de cadastro do motorista
    path('cadastro/ser_motorista', views.passageiro_to_motorista, name='cadastro_ser_motorista'),   # url de update do Profile para cadastro do Motorista
    path('cadastro/localizacao', views.adicionar_localizacao, name='adicionar_localizacao'),        # url de adicionar localizacao

    path('caronas_disponiveis', views.caronas_disponiveis, name='caronas_disponiveis'),             # url de caronas disponiveis

    path('adicionar_carona', views.adicionar_carona, name='adicionar_carona'),                      # url de adicionar carona

    path('atualizar_dados', views.atualizar_dados, name='atualizar_dados'),                         # url de atualizar dados cadastrais
    path('alterar_senha', views.alterar_senha, name='alterar_senha'),                               # url de alterar senha
]