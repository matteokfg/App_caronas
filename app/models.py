from django.db import models
from django.conf import settings
from django.utils import timezone
# extensao do usuario django
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# field do cpf no banco de dados no django
from localflavor.br.models import BRCPFField

#<---------------------------------- model user ------------------------------------------>


class Profile_usuario(models.Model):
    # Extensao do usuario padrao ja existente no django
    # faz a relacao de um para um entre o model inicial do django de usuarios com esse que adiciona mais campos relacionados ao usuario
    user = models.OneToOneField(
        User, 
        on_delete=models.PROTECT,
        verbose_name="user_fk",
        help_text="Chave estrangeira conectando o user do django ao perfil do usuario",
    )

    cpf_user = BRCPFField(
        primary_key=True,
        verbose_name="CPF_pk",
        help_text="Coluna com CPF do usuario",
    )


    RELATION_WITH_UNISO = (
        ('A', 'Aluno'),
        ('F', 'Funcionario'),
        ('T', 'Terceiro'),
    )

    relation_with_uniso_user = models.CharField(
        max_length=1,
        choices=RELATION_WITH_UNISO,
        verbose_name="Relacao UNISO",
        help_text="Coluna com a relacao do usuario com a UNISO",
    )


    GENERO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    genero_user = models.CharField(
        max_length=1,
        choices=GENERO,
        verbose_name="Genero",
        help_text="Coluna com o genero do usuario",
    )

    ativo = models.BooleanField()

    eh_motorista = models.BooleanField()

    def __str__(self):
        return self.user

# a tabela Usuario vai ser atualizada automaticamente quando o User for atualizado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile_usuario.objects.create(user=instance)
# lugar aonde vi essas funcoes: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#<---------------------------------- fim model user -------------------------------------->
#<---------------------------------- model motorista ------------------------------------->

class Motorista(models.Model):

    user_id = models.OneToOneField(
        Profile_usuario,
        on_delete=models.PROTECT,
        verbose_name="ID",
        help_text="Coluna com o id do usuario que e motorista",
    )


    # photo_car = models.FileField(
    ## os arquivos nao vao ser salvos no BD, ver onde tem media_root e media_url
    #   upload_to=#MEDIA_ROOT
    ## o BD vai apenas salvar o caminho para o arquivo
    # )

    placa = models.CharField(
        default='AAA-0000',
        max_length=8,
        verbose_name="Placa",
        help_text="Coluna com a placa do carro da carona, sendo padrao: 'XXX-0000'.",
    )

    def __str__(self):
        return self.user_id

#<---------------------------------- fim model motorista --------------------------------->
#<---------------------------------- model carona ---------------------------------------->

class Carona(models.Model):
    """Tabela que vai guardar os atributos do evento da carona"""
    
    user_motorista = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name="Usuario",
        help_text="Coluna com o motorista da carona",
    )

    # location_inicial =           | localizacao inicial do carro
    # location_to =            | destino da carona



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
        help_text="Coluna com o numero da lotacao do carro da carona",
    )

    date_inicial_carona = models.DateTimeField(
        default=timezone.now,
        verbose_name="Dat   a de inicio",
        help_text="Data e hora iniciais da carona",
    )

    date_final_carona = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data final",
        help_text="Data e hora finais da carona",
    )

    @property
    def carona_duration(self):
        # o tempo vai ser guardado em segundos (decimal)

        return self.date_final_carona - self.date_inicial_carona
        #max_digits=7,
        #decimal_places=1,
        #verbose_name="Duracao",
        #help_text="Coluna com a duracao da carona(ms)"

    def __str__(self):
        return f"Carona feita por {self.user_motorista}, na data {self.date_inicial_carona}, durando {self.carona_duration()}."

#<---------------------------- fim model carona ---------------------------------------->



