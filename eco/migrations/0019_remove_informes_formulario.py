# Generated by Django 5.1.2 on 2024-11-25 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0018_informes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informes',
            name='formulario',
        ),
    ]
