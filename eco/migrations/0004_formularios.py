# Generated by Django 4.1.3 on 2024-09-27 00:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0003_materiales_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formularios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('materiales', models.ManyToManyField(to='eco.materiales')),
            ],
        ),
    ]
