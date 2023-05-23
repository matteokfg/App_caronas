from django.db import models
from django.conf import settings
from django.utils import timezone
# extensao do usuario django
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# field do cpf no banco de dados no django
from localflavor.br.models import BRCPFField
# arquivo que contem as tabelas do banco em modo orientacao a objetos do python/django

#<---------------------------------- model user ------------------------------------------>

class Profile(models.Model):
    # Extensao do usuario padrao ja existente no django
    # faz a relacao de um para um entre o model inicial do django de usuarios com esse que adiciona mais campos relacionados ao usuario
    user = models.OneToOneField(
        User, 
        on_delete=models.PROTECT,
        related_name="profile",
        verbose_name="Usuário",
        help_text="Chave estrangeira conectando o usuário do django ao perfil do usuário.",
    )

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

# a tabela Profile vai ser atualizada automaticamente quando o User for atualizado
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

    profile = models.OneToOneField(
        Profile,
        on_delete=models.PROTECT,
        related_name="motorista",
        verbose_name="ID",
        help_text="Coluna com o id do usuario que e motorista",
    )

    foto_motorista = models.ImageField(
        upload_to="uploads/foto_motorista/",
        blank=True,
        null=True,
    )

    foto_carro = models.ImageField(
        upload_to="uploads/foto_carro/",
        blank=True,
        null=True,
    )

    foto_cnh = models.ImageField(
        upload_to="uploads/foto_documento_cnh/",
        blank=True,
        null=True,
    )

    placa = models.CharField(
        default='AAA-0000',
        max_length=8,
        verbose_name="Placa do carro",
        help_text="Coluna com a placa do carro da carona, sendo padrao: 'XXX-0000'.",
    )

    def __str__(self):
        return str(self.profile)

@receiver(post_save, sender=Profile)
def create_user_motorista(sender, instance, created, **kwargs):
    if created:
        Motorista.objects.create(profile=instance)
# lugar aonde vi essas funcoes: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=Profile)
def save_user_motorista(sender, instance, **kwargs):
    instance.motorista.save()
#<---------------------------------- fim model motorista --------------------------------->
#<---------------------------------- inicio model localizacao----------------------------->
class Localizacao(models.Model):
    """Tabela que vai guardar as localizacoes utilizadas nas caronas, vai ser populada pela Google Maps API."""

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

    def location(self):
        # metodo retorna coordenadas
        return f"Localizacao: {self.latitude} {self.longitude}"
#<---------------------------------- fim model localizacao-------------------------------->
#<---------------------------------- model carona ---------------------------------------->

class Carona(models.Model):
    """Tabela que vai guardar os atributos do evento da carona"""

    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.PROTECT,
        related_name="carona",
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



