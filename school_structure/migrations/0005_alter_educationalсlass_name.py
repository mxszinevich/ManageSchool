# Generated by Django 3.2.7 on 2021-09-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_structure', '0004_alter_educationalсlass_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalсlass',
            name='name',
            field=models.CharField(error_messages={'unique': 'Класс с таким именем уже существует'}, max_length=300, unique=True, verbose_name='Название класса'),
        ),
    ]
