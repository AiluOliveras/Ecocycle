# Generated by Django 5.1.2 on 2024-11-25 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0023_informes_abierto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='informes',
            old_name='abierto',
            new_name='pagado',
        ),
    ]
