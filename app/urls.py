from django.urls import path
from . import views

#This file defines the URL patterns for the app. URL patterns map URLs to views, which are Python functions that handle HTTP requests and return HTTP responses. 
#In this file, we define a single URL pattern that maps the root URL ('/') to the 'index' view function. This means that when a user visits the root URL of the app, the 'index' view function will be called to handle the request.
#URL patterns are an essential part of any Django project, as they allow us to define the structure and behavior of our web application's URLs. By defining URL patterns in this file, we can ensure that our app responds correctly to incoming requests and provides a consistent user experience.

urlpatterns = [
    path('', views.inicio_index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('cadastro', views.cadastro, name='cadastro'),
    path('cadastro/passageiro', views.cadastro_passageiro, name='cadastro_passageiro'),
    path('cadastro/motorista', views.cadastro_motorista, name='cadastro_motorista'),
    path('cadastro/ser_motorista', views.passageiro_to_motorista, name='cadastro_ser_motorista'),

    path('caronas_disponiveis', views.caronas_disponiveis, name='caronas_disponiveis'),

    path('adicionar_carona', views.adicionar_carona, name='adicionar_carona'),

    path('atualizar_dados', views.atualizar_dados, name='atualizar_dados'),
    path('alterar_senha', views.alterar_senha, name='alterar_senha'),
]