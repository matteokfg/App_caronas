# Generated by Django 3.2.14 on 2023-05-17 20:56

from django.db import migrations
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20230516_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cpf_user',
            field=localflavor.br.models.BRCPFField(help_text='Coluna com CPF do usuario', max_length=14, verbose_name='CPF'),
        ),
    ]
