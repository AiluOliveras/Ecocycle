# Generated by Django 5.1.2 on 2024-11-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0031_solicitudes_red_id_externo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiposmateriales',
            name='trabajado',
            field=models.BooleanField(default=False),
        ),
    ]