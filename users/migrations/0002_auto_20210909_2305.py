# Generated by Django 3.2.7 on 2021-09-09 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_structure', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffuser',
            name='school',
        ),
        migrations.AddField(
            model_name='staffuser',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school_structure.school', verbose_name='Образовательная организация'),
        ),
    ]
