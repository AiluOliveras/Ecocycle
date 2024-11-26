# Generated by Django 5.1.2 on 2024-11-25 20:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0028_alter_procesos_estado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Punto_proceso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('id_bonita', models.IntegerField()),
                ('iniciado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('punto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.punto_recoleccion')),
            ],
        ),
    ]
