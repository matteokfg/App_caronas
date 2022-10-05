from django.contrib import admin
from .models import (
    Motorista,
    Profile_usuario,
    Carona,
)


admin.site.register(Profile_usuario)
admin.site.register(Motorista)
admin.site.register(Carona)