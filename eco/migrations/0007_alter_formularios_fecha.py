# Generated by Django 4.1.3 on 2024-09-30 01:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0006_alter_materiales_formulario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formularios',
            name='fecha',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]