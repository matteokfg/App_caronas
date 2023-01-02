from django.contrib import admin
from .models import (
    Motorista,
    Profile,
    Carona,
)


admin.site.register(Profile)
admin.site.register(Motorista)
admin.site.register(Carona)