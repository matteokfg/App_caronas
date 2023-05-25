# Generated by Django 3.2.14 on 2023-05-22 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0011_alter_profile_eh_motorista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carona',
            name='date_final_carona',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data e hora finais da carona.', verbose_name='Data final'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='date_inicial_carona',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data e hora iniciais da carona.', verbose_name='Data de inicio'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='inicial_location',
            field=models.ForeignKey(help_text='Coluna com oa localização (latitude e longitude) inicial da carona.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='localizacao_inicial', to='app.localizacao', verbose_name='Localização inicial'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='location_final',
            field=models.ForeignKey(help_text='Coluna com oa localização (latitude e longitude) final da carona.', null=True, on_delete=django.db.models.deletion.PROTECT, to='app.localizacao', verbose_name='Localizacao final'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='lotation',
            field=models.IntegerField(choices=[(1, 'Mais Um'), (2, 'Mais Dois'), (3, 'Mais Tres'), (4, 'Mais Quatro'), (5, 'Mais Cinco'), (6, 'Mais Seis')], default=3, help_text='Coluna com o número da lotação do carro da carona.', verbose_name='Lotacao'),
        ),
        migrations.AlterField(
            model_name='carona',
            name='motorista',
            field=models.ForeignKey(help_text='Coluna com o motorista da carona.', on_delete=django.db.models.deletion.PROTECT, to='app.motorista', verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='motorista',
            name='foto_motorista',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/foto_motorista/'),
        ),
        migrations.AlterField(
            model_name='motorista',
            name='placa',
            field=models.CharField(default='AAA-0000', help_text="Coluna com a placa do carro da carona, sendo padrao: 'XXX-0000'.", max_length=8, verbose_name='Placa do carro'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cpf_user',
            field=localflavor.br.models.BRCPFField(help_text='Coluna com CPF do usuário.', max_length=14, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='genero_user',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], help_text='Coluna com o gênero do usuário.', max_length=1, verbose_name='Gênero'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='relation_with_uniso_user',
            field=models.CharField(choices=[('A', 'Aluno'), ('F', 'Funcionario'), ('T', 'Terceiro')], help_text='Coluna com a relação do usuário com a UNISO.', max_length=1, verbose_name='Relação com a UNISO'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(help_text='Chave estrangeira conectando o usuário do django ao perfil do usuário.', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
