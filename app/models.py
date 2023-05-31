from typing import Any
from django.db import models
from django.conf import settings
from django.utils import timezone
# extensao do usuario django
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# field do cpf no banco de dados no django
from localflavor.br.models import BRCPFField
# modificador de nome da imagem
from django.utils.deconstruct import deconstructible
import uuid
import os
# modificador de tamanho da imagem
from PIL import Image


# modificador do nome da imagem para um codigo unico
@deconstructible
class DynamicUploadTo():
    def __init__(self, upload_to):
        self.upload_to = upload_to

    def __call__(self, instance, filename):
        generated_uuid = uuid.uuid4()
        extension = filename.split('.')[-1]
        new_filename = f"{generated_uuid}.{extension}"
        return os.path.join(self.upload_to, new_filename)

# modificador para cada tipo de imagem do Motorista
Motorista_foto_motorista_upload_to = DynamicUploadTo("uploads/foto_motorista/")
Motorista_foto_carro_upload_to = DynamicUploadTo("uploads/foto_carro/")
Motorista_foto_cnh_upload_to = DynamicUploadTo("uploads/foto_documento_cnh/")


#<---------------------------------- model user ------------------------------------------>

class Profile(models.Model):
    """Extensao do usuario padrao ja existente no django.
       Faz a relacao de um para um entre o model inicial do django de usuarios com esse que adiciona mais campos relacionados ao usuario."""

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,  # se apagar o user, vai apagar o profile
        related_name="profile",  # com profile, consigo os dados do user, sem querys extras no BD
        verbose_name="Usuário",
        help_text="Chave estrangeira conectando o usuário do django ao perfil do usuário.",
    )
    # campo do CPF
    cpf_user = BRCPFField(
        verbose_name="CPF",
        help_text="Coluna com CPF do usuário.",
    )

    RELATION_WITH_UNISO = (
        ('A', 'Aluno'),
        ('F', 'Funcionario'),
        ('T', 'Terceiro'),
    )

    relation_with_uniso_user = models.CharField(
        max_length=1,
        choices=RELATION_WITH_UNISO,
        verbose_name="Relação com a UNISO",
        help_text="Coluna com a relação do usuário com a UNISO.",
    )

    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    genero_user = models.CharField(
        max_length=1,
        choices=GENERO,
        verbose_name="Gênero",
        help_text="Coluna com o gênero do usuário.",
    )

    eh_motorista = models.BooleanField(
        null=True,
        verbose_name="Quer ser motorista?"
    )

    def __str__(self):
        return self.user.username

# a tabela Profile vai ser criada/atualizada automaticamente quando o User for criado/atualizado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# lugar aonde vi essas funcoes: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#<---------------------------------- fim model user -------------------------------------->
#<---------------------------------- model motorista ------------------------------------->

class Motorista(models.Model):
    """Tabela do Motorista, model de Motorista, caso o usuario seja motorista, deverá preencher esses dados."""

    profile = models.OneToOneField(  # relacao com o Profile
        Profile,
        on_delete=models.CASCADE,  # se apagar profile, apaga motorista
        related_name="motorista",  # consegue dados de profile, sem queries extras
        verbose_name="ID",
        help_text="Coluna com o id do usuário, que é o motorista.",
    )

    foto_motorista = models.ImageField(
        upload_to=Motorista_foto_motorista_upload_to,
        blank=True,
        null=True,
        verbose_name="Sua foto:",
    )

    foto_carro = models.ImageField(
        upload_to=Motorista_foto_carro_upload_to,
        blank=True,
        null=True,
        verbose_name="Foto do carro da carona:",
    )

    foto_cnh = models.ImageField(
        upload_to=Motorista_foto_cnh_upload_to,
        blank=True,
        null=True,
        verbose_name="Foto da sua CNH:",
    )

    placa = models.CharField(
        default='AAA-0000',
        max_length=8,
        verbose_name="Placa do carro",
        help_text="Coluna com a placa do carro da carona, seguindo o padrão: 'XXX-0000'.",
    )

    def __str__(self):
        return str(self.profile)
# se criar Profile, cria Motorista
@receiver(post_save, sender=Profile)
def create_user_motorista(sender, instance, created, **kwargs):
    if created:
        Motorista.objects.create(profile=instance)
# lugar aonde vi essas funcoes: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone


# Referencia https://stackoverflow.com/a/56110972
# depois que salvar no banco de dados as imagens, altera elas para terem um tamanho menor, para ocupar menos espaco no HD
@receiver(post_save, sender=Motorista)
def resize_images(sender, instance, **kwargs):                                          # funcao para redimensionar os campos de imagem, depois de salvos no BD e no disco
    fields_to_resize = {                                                                # dicionario contendo os tres campos de imagefield, de Motorista, e cada um tem seu valor a ser redimensionado
        'foto_motorista': {
            'max_width': 200,
            'max_height': 200,
        },
        'foto_carro': {
            'max_width': 400,
            'max_height': 400,
        },
        'foto_cnh': {
            'max_width': 400,
            'max_height': 400,
        },
    }

    for fieldname, image_sizes in fields_to_resize.items():                             # loop for para cada item do dicionario a cima
        imagefield = getattr(instance, fieldname)                                       # acessando o campo pela string fieldname

        if not isinstance(imagefield, models.ImageField):                               # verifica se o campo é um imagefield
            break

        image_max_width = image_sizes.get('max_width', settings.MAX_WIDTH)              # tenta pegar o valor do dicionario, senao conseguir, pegar o valor das settings
        image_max_height = image_sizes.get('max_height', settings.MAX_HEIGHT)           # tenta pegar o valor do dicionario, senao conseguir, pegar o valor das settings

        if imagefield and ((imagefield.width > image_max_width) or (imagefield.height > image_max_height)):  # verifica se o campo nao eh nulo, e se ultrapassa algum limite
            img = Image.open(imagefield.path)
            img.thumbnail((image_max_width, image_max_height))                          # redimenciona a imagem
            img.save(imagefield.path, quality=95)                                       # salva, com a qualidade em 95%
            img.close()                                                                 # fecha o objeto


#<---------------------------------- fim model motorista --------------------------------->
#<---------------------------------- inicio model localizacao----------------------------->
class Localizacao(models.Model):
    """Tabela que vai guardar as localizacoes utilizadas nas caronas."""

    latitude = models.DecimalField(
        max_digits=11,
        decimal_places=7,
        verbose_name="Latitude",
        help_text="Representa a parte da coordenada: Latitude.",
    )

    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=7,
        verbose_name="Longitude",
        help_text="Representa a parte da coordenada: Longitude.",
    )

    def __str__(self):
        # metodo retorna coordenadas, quado mostrar o objeto nas telas
        return f"{self.latitude} e {self.longitude}"
#<---------------------------------- fim model localizacao-------------------------------->
#<---------------------------------- model carona ---------------------------------------->

class Carona(models.Model):
    """Tabela que vai guardar os atributos do evento da carona"""

    motorista = models.ForeignKey(  # faz relacao com motorista
        Motorista,
        on_delete=models.PROTECT,  # se apagar o motorista, protege os dados da tabela Carona
        related_name="carona",  # consegue os dados de motorista, sem queries extras
        verbose_name="Usuario",
        help_text="Coluna com o motorista da carona.",
    )

    #localizacao inicial do carro, faz referencia a tabela que guarda as coordenadas (https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects)
    inicial_location = models.ForeignKey(
        Localizacao,
        on_delete=models.PROTECT,
        related_name="localizacao_inicial",
        null=True,
        verbose_name="Localização inicial",
        help_text="Coluna com oa localização (latitude e longitude) inicial da carona.",
    )  

    #localizacao destino da carona ,faz referencia a tabela que guarda a localizacao
    location_final = models.ForeignKey(
        Localizacao,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Localizacao final",
        help_text="Coluna com oa localização (latitude e longitude) final da carona.",
    )


    class Lotacao(models.IntegerChoices):
        MAIS_UM = 1,
        MAIS_DOIS = 2,
        MAIS_TRES = 3,
        MAIS_QUATRO = 4,
        MAIS_CINCO = 5,
        MAIS_SEIS = 6,
    # loatacao da carona
    lotation = models.IntegerField(
        choices=Lotacao.choices,
        default=Lotacao.MAIS_TRES,
        verbose_name="Lotacao",
        help_text="Coluna com o número da lotação do carro da carona.",
    )

    date_inicial_carona = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de início",
        help_text="Data e hora iniciais da carona.",
    )

    date_final_carona = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data final",
        help_text="Data e hora finais da carona.",
    )

    @property
    def carona_duration(self):
        # o tempo vai ser guardado em segundos (decimal)
        return self.date_final_carona - self.date_inicial_carona
    
    def carona_location(self):
        # metodo retorna coordenadas (iniciais e finais)
        return f"Localizacao inicial: {self.inicial_location.latitude} {self.inicial_location.longitude} e Localizacao final: {self.location_final.latitude} {self.location_final.longitude}"

    def __str__(self):
        return f"Carona feita por {self.motorista}, na data {self.date_inicial_carona}, durando {self.carona_duration}."

#<---------------------------- fim model carona ---------------------------------------->



