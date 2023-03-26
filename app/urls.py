from django.urls import path
from . import views

urlpatterns = [
    path('', views.caronas_disp, name='caronas_disp'),
]