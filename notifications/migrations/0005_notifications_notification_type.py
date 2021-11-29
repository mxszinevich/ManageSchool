# Generated by Django 3.2.7 on 2021-11-29 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notifications_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='notification_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Уведомление о новых пользователях')], null=True, verbose_name='Тип уведомления'),
        ),
    ]