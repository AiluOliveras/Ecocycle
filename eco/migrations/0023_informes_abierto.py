# Generated by Django 5.1.2 on 2024-11-25 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0022_tiposmateriales_precio_por_kg'),
    ]

    operations = [
        migrations.AddField(
            model_name='informes',
            name='abierto',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
