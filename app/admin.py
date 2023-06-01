from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Motorista,
    Profile,
    Localizacao,
    Carona,
)


class MotoristaAdmin(admin.ModelAdmin):
    readonly_fields = ['foto_motorista_image', 'foto_carro_image', 'foto_cnh_image']

    def foto_motorista_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.foto_motorista.url,
            width=obj.foto_motorista.width,
            height=obj.foto_motorista.height,
            )
    )
    def foto_carro_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.foto_carro.url,
            width=obj.foto_carro.width,
            height=obj.foto_carro.height,
            )
    )
    def foto_cnh_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.foto_cnh.url,
            width=obj.foto_cnh.width,
            height=obj.foto_cnh.height,
            )
    )


admin.site.register(Profile)
admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Localizacao)
admin.site.register(Carona)