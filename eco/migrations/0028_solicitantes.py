# Generated by Django 5.1.2 on 2024-11-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0027_informes_evaluacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=253)),
            ],
        ),
    ]
