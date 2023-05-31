from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# nos templates: em tags 'a', a atributo 'href', vai ter seu valor: '{% url 'nome_da_url' %}'
# quando o usuario clicar nesse link, a requisicao vai passar pelo Middleware, vai chegar aqui, procurando pelo seu padrao de url
# lista de padroes de url
urlpatterns = [
    path('admin/', admin.site.urls),                                            # se for da parte administrativa, em que apenas usuarios Admin tem acesso, cai nesse padrao, onde comeca com 'admin/'
    path('', include('app.urls')),                                              # se nao tiver nada, e a area normal do site, para usuario passageiros e motoristas, que vai usar as urls do 'app/urls.py'
    path('__debug__/', include('debug_toolbar.urls')),                          # se for a parte de debug, vai aparecer essa ferrementa de DEBUG
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # para arquivos origidos do upload dos usuarios, use essa url