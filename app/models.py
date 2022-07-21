from django.conf import settings
from django.db import models
from django.utils import timezone
from localflavor.br.models import BRCPFField

#<---------------------------------- model user ------------------------------------------>

class Usuario(models.Model):


    cpf_user = BRCPFField(
        verbose_name="CPF",
        help_text="Coluna com CPF do usuario",
    )
    # cpf_user = models.PositiveBigIntegerField(
    #     MaxValueValidator=10000000000,
    #     unique=True,
    #     one_to_many=True,
    #     verbose_name="CPF",
    #     help_text="Coluna com CPF do usuario"
    # )

    nome_user = models.CharField(
        max_length=100,
        verbose_name="Nome",
        help_text="Coluna com o nome do usuario",
    )

    email_user = models.EmailField(
        max_length=254,
        verbose_name="Email",
        help_text="Coluna com o email do usuario",
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

    #models.?   ->  senha

    motorista = models.BooleanField()

    def __str__(self):
        return self.nome_user

#<---------------------------------- fim model user -------------------------------------->
#<---------------------------------- model motorista ------------------------------------->

class Motorista(models.Model):

    user_id = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="ID",
        help_text="Coluna com o id do usuario que e motorista",
    )

    # if user_id.motorista:
    #     # photo_car = models.ImageField(

    #     # )       #-> fotos(cnh, carro, documento_uniso)

    #     # photo_CNH = models.ImageField(

    #     # )       #-> fotos(cnh, carro, documento_uniso)

    #     # photo_doc = models.ImageField(

    #     # )       #-> fotos(cnh, carro, documento_uniso)

    #     placa = models.CharField(
    #         max_length=9,
    #         verbose_name="Placa",
    #         help_text="Coluna com a placa do carro da carona, sendo padrao: 'XXX-0000'.",
    #     )         #->   placa

    def __str__(self):
        return self.user_id

#<---------------------------------- fim model motorista --------------------------------->
#<---------------------------------- model carona ---------------------------------------->

class Carona(models.Model):
    
    
    user_motorista = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        help_text="Coluna com o motorista da carona",
        )

#     # location_now =           | localizacao atual do carro
#     # location_to =            | destino da carona

#     placa = NAO PRECISA, ja vai estar conactado palo usuario(motorista)

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

    date_carona = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data",
        help_text="Data da carona",
    )

    def __str__(self):
        return f"Carona feita por {self.user_motorista}, na data {self.date_carona}"

#<---------------------------- fim model carona ---------------------------------------->



