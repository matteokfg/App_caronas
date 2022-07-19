from django.conf import settings
from django.db import models
from django.forms import EmailField
from django.utils import timezone

#<---------------------------------- model user ------------------------------------------>

class Usuario(models.Model):

    cpf_user = models.PositiveBigIntegerField(
        MaxValueValidator=10000000000,
        unique=True,
        one_to_many=True,
        verbose_name="CPF",
        help_text="Coluna com CPF do usuario"
    )

    nome_user = models.CharField(
        max_length=100,
        verbose_name="Nome",
        help_text="Coluna com o nome do usuario"
    )

    email_user = models.EmailField(
        max_length=254,
        verbose_name="Email",
        help_text="Coluna com o email do usuario"
    )


    RELATION_WITH_UNISO = (
        ('A', 'Aluno'),
        ('F', 'Funcionario'),
        ('T', 'Terceiro')
    )


    relation_with_uniso_user = models.CharField(
        max_length=1,
        choices=RELATION_WITH_UNISO,
        verbose_name="Relacao UNISO",
        help_text="Coluna com a relacao do usuario com a UNISO"
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
        help_text="Coluna com o genero do usuario"
    )

    #models.?   ->  senha

#------------------deve ser no usuario ou uma nova coluna com apenas o motorista?--------

    motorista = models.BooleanField()

#    def motorista_ou_carona(self,):
#        if self.motorista:
#            foto = models.ImageField?  -> fotos(cnh, carro, documento_uniso)
#            placa = models.CharField(
#                max_length=9,
#                help_text="Coluna com a placa do carro da carona, sendo padrao: 'XXX-0000'."
#            )   -> placa
#             pass
#         else:
#             pass

                #-----------------fim-------------------



#<---------------------------------- fim model user -------------------------------------->


#<---------------------------------- model carona ---------------------------------------->

# class Carona(models.Model):
    
#     class Lotacao(models.IntegerChoices):
#         MAIS_UM = 1,
#         MAIS_DOIS = 2,
#         MAIS_TRES = 3,
#         MAIS_QUATRO = 4,
#         MAIS_CINCO = 5,
#         MAIS_SEIS = 6
    
#     author = models.ForeignKey(
#         Usuario, 
#         on_delete=models.CASCADE,
#         help_text="Coluna com o motorista da carona"
#         )

#     # location_now =           | localizacao atual do carro
#     # location_to =            | destino da carona

#     placa = NAO PRECISA, ja vai estar conactado palo usuario(motorista)

#     lotation = models.IntegerField(
#         choices=Lotacao.choices,
#         default=Lotacao.MAIS_TRES,
#         help_text="Coluna com o numero da lotacao do carro da carona"
#         )

#<---------------------------- fim model carona ---------------------------------------->


# --------------- lugar ainda nao terminado, n colocar na branch! --------------------

