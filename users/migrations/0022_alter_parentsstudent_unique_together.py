# Generated by Django 3.2.7 on 2021-11-13 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_parentsstudent_phone_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='parentsstudent',
            unique_together={('first_name', 'last_name', 'phone_number')},
        ),
    ]