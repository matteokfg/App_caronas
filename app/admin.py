from django.contrib import admin
from .models import (
    Motorista,
    Profile,
    Localizacao,
    Carona,
)

# registers the models "Motorista", "Profile", and "Carona" with the Django admin site. This allows administrators to view, add, edit, and delete instances of these models through the Django admin interface. The registration is done using the admin.site.register() function provided by Django.

admin.site.register(Profile)
admin.site.register(Motorista)
admin.site.register(Localizacao)
admin.site.register(Carona)