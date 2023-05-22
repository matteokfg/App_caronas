from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Motorista,
    Profile,
    Localizacao,
    Carona,
)

# registers the models "Motorista", "Profile", and "Carona" with the Django admin site. This allows administrators to view, add, edit, and delete instances of these models through the Django admin interface. The registration is done using the admin.site.register() function provided by Django.

class MotoristaAdmin(admin.ModelAdmin):
    readonly_fields = ['foto_motorista_image']
    def foto_motorista_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.foto_motorista.url,
            width=obj.foto_motorista.width,
            height=obj.foto_motorista.height,
            )
    )
    
    


admin.site.register(Profile)
admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Localizacao)
admin.site.register(Carona)