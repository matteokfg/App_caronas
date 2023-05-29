# Generated by Django 3.2.14 on 2023-05-26 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0020_auto_20230526_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motorista',
            name='profile',
            field=models.OneToOneField(help_text='Coluna com o id do usuário, que é o motorista.', on_delete=django.db.models.deletion.CASCADE, related_name='motorista', to='app.profile', verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(help_text='Chave estrangeira conectando o usuário do django ao perfil do usuário.', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
