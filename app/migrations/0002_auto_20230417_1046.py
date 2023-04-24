# Generated by Django 3.2.14 on 2023-04-17 13:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Localizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=7, help_text='Representa a parte da coordenada, Latitude (em float), retornada pela API', max_digits=11, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=7, help_text='Representa a parte da coordenada, Longitude (em float), retornada pela API', max_digits=11, verbose_name='Longitude')),
            ],
        ),
        migrations.AlterField(
            model_name='carona',
            name='date_inicial_carona',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data e hora iniciais da carona', verbose_name='Data de inicio'),
        ),
        migrations.AddField(
            model_name='carona',
            name='inicial_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='localizacao_inicial', to='app.localizacao'),
        ),
        migrations.AddField(
            model_name='carona',
            name='location_final',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.localizacao'),
        ),
    ]