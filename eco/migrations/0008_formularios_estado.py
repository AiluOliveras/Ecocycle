# Generated by Django 4.1.3 on 2024-09-30 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0007_alter_formularios_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='formularios',
            name='estado',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
