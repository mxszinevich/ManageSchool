# Generated by Django 3.2.7 on 2021-09-14 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_structure', '0003_alter_subject_direction_science'),
        ('users', '0005_auto_20210914_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffuser',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='school_structure.school', verbose_name='Образовательная организация'),
        ),
    ]
