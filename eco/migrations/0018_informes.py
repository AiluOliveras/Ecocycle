# Generated by Django 5.1.2 on 2024-11-25 00:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0017_formularios_procesado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Informes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('cant_materiales_fallidos', models.IntegerField()),
                ('kg_faltantes_total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cant_materiales_exitosos', models.IntegerField()),
                ('cant_mats_no_recibidos', models.IntegerField()),
                ('monto_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('formulario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='eco.formularios')),
            ],
        ),
    ]
