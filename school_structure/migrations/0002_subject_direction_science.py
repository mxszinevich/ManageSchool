# Generated by Django 3.2.7 on 2021-09-13 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_structure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='direction_science',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_structure.directionscience', verbose_name='Учебное направление'),
        ),
    ]
