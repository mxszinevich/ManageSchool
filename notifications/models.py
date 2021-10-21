from django.core.mail import send_mail
from django.db import models

from config import settings
from users.models import User


class Email(models.Model):
    theme = models.CharField(verbose_name='Тема письма', max_length=200)
    body = models.TextField(verbose_name='Тело письма', blank=True, null=True)
    recipients = models.ManyToManyField(User, verbose_name='Получатель', related_name='emails')

    def __str__(self):
        return self.theme

    def send_email(self, *args, **kwargs):
        recipients = list(self.recipients.only('email').all().values_list('email', flat=True))
        send_mail(self.theme, self.body, settings.EMAIL_HOST_USER, recipients)



