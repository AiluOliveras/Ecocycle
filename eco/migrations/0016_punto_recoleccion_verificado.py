# Generated by Django 5.1.2 on 2024-11-23 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0015_materiales_material_recibido'),
    ]

    operations = [
        migrations.AddField(
            model_name='punto_recoleccion',
            name='verificado',
            field=models.BooleanField(default=False),
        ),
    ]
