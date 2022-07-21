# Generated by Django 3.2.14 on 2022-07-21 19:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import localflavor.br.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_user', localflavor.br.models.BRCPFField(help_text='Coluna com CPF do usuario', max_length=14, verbose_name='CPF')),
                ('nome_user', models.CharField(help_text='Coluna com o nome do usuario', max_length=100, verbose_name='Nome')),
                ('email_user', models.EmailField(help_text='Coluna com o email do usuario', max_length=254, verbose_name='Email')),
                ('relation_with_uniso_user', models.CharField(choices=[('A', 'Aluno'), ('F', 'Funcionario'), ('T', 'Terceiro')], help_text='Coluna com a relacao do usuario com a UNISO', max_length=1, verbose_name='Relacao UNISO')),
                ('genero_user', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], help_text='Coluna com o genero do usuario', max_length=1, verbose_name='Genero')),
                ('e_motorista', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Motorista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(help_text='Coluna com o id do usuario que e motorista', on_delete=django.db.models.deletion.CASCADE, to='app.usuario', verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Carona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lotation', models.IntegerField(choices=[(1, 'Mais Um'), (2, 'Mais Dois'), (3, 'Mais Tres'), (4, 'Mais Quatro'), (5, 'Mais Cinco'), (6, 'Mais Seis')], default=3, help_text='Coluna com o numero da lotacao do carro da carona', verbose_name='Lotacao')),
                ('date_carona', models.DateTimeField(default=django.utils.timezone.now, help_text='Data da carona', verbose_name='Data')),
                ('user_motorista', models.ForeignKey(help_text='Coluna com o motorista da carona', on_delete=django.db.models.deletion.CASCADE, to='app.usuario', verbose_name='Usuario')),
            ],
        ),
    ]
