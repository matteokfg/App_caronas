# Generated by Django 3.2.14 on 2022-12-22 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_usuario',
            name='ativo',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='profile_usuario',
            name='eh_motorista',
            field=models.BooleanField(null=True),
        ),
    ]
