# Generated by Django 5.1.2 on 2024-11-24 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0016_punto_recoleccion_verificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='formularios',
            name='procesado',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]