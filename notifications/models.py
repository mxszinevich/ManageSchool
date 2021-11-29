from datetime import datetime, timedelta
from django.db import models
from users.models import User



class Notifications(models.Model):
    TYPE_NEW_USERS = 1
    notifications_types = (
        (TYPE_NEW_USERS, 'Уведомление о новых пользователях'),
    )

    theme = models.CharField(verbose_name='Тема письма', max_length=200)
    body = models.TextField(verbose_name='Тело письма', blank=True, null=True)
    recipients = models.ManyToManyField(User, verbose_name='Получатель', related_name='emails')
    date_time = models.DateTimeField(verbose_name='Время отправки уведомления', null=True, blank=True)
    status = models.BooleanField(verbose_name='Статус отправки', default=False)
    notification_type = models.IntegerField(verbose_name='Тип уведомления', choices=notifications_types, null=True, blank=True)

    def __str__(self):
        return self.theme

    def create_send_email(self):
        """
        Отправка нотификации получателям
        """
        from users.tasks import send_email

        if self is not None and self.recipients:
            for recipient in self.recipients.all():
                send_email.apply_async(
                    [self.id, recipient.email],
                    eta=datetime.utcnow() + timedelta(minutes=1),
                    queue='emails'
                )

    @classmethod
    def get_basiс_data_notification(cls, type_notification=None, count_new_users=0):
        notification_data = {
            Notifications.TYPE_NEW_USERS: {
                    'theme': 'Уведомление о новых пользователях',
                    'body': 'Кол-во новых пользователей в системе: {count}'.format(count=count_new_users),
                    'status': False,
                    'notification_type': cls.TYPE_NEW_USERS
                }
        }
        if type_notification is not None:
            try:
                return notification_data[type_notification]
            except KeyError:
                # TODO  добавить logger()
                raise KeyError('Отсутсвующий тип нотификации')

        return notification_data







