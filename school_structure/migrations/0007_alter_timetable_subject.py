# Generated by Django 3.2.7 on 2021-09-27 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_structure', '0006_alter_educationalсlass_timetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='subject',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school_structure.subject', verbose_name='Предмет'),
        ),
    ]
