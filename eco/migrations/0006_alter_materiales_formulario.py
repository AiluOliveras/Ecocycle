# Generated by Django 4.1.3 on 2024-09-27 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0005_remove_formularios_materiales_materiales_formulario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiales',
            name='formulario',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='eco.formularios'),
        ),
    ]
