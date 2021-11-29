from datetime import datetime, timedelta

import pandas
from django.core.mail import send_mail
from django.db.models import Q

from config.celery import celery_app
from config import settings

from notifications.models import Notifications

from users.models import User, StaffUser


class TemplateReports:
    def __init__(self, *args, **kwargs):
        self.fields_names = []
        for model in args:
            self.fields_names += [field.name for field in model._meta.get_fields()]


@celery_app.task
def generate_students_reports():
    """
    Метод создания отчетов по студентам
    """
    from users.models import User, Student, StaffUser
    base_model = Student
    table_reports = [base_model, User]
    template = TemplateReports(*table_reports)
    data_frame = {}
    table_data = Student.objects.select_related('user').order_by('id').values()
    for column_name in template.fields_names:
        data_frame[column_name] = [row_data.get(column_name) for row_data in table_data]
        data_frame[column_name] = [User.objects.filter(id=row_data.get('user_id')).values().first().get(column_name) for row_data in table_data]
    pandas.DataFrame(data_frame).to_excel(settings.MEDIA_ROOT + '/reports/reports.xlsx')


@celery_app.task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_email(notification_id, recipient_email):
    try:
        notification = Notifications.objects.get(id=notification_id)
        send_mail(notification.theme, notification.body, settings.EMAIL_HOST_USER, [recipient_email])
        notification.status = True
        notification.date_time = datetime.now()
        notification.save(update_fields=['status', 'date_time'])

    except Notifications.DoesNotExist:
        # TODO logger нотификация не найдена
        pass
    except:
        pass


@celery_app.task
def process_initial_notifications_about_new_users():
    """
    Метод создания уведомлений о новых зарегистрированных пользователях
    Запускается каждый день в 0 0 * * *
    """
    base_query = Q(is_account_confirmation=False) & Q(registration_date__lte=datetime.now())
    type_days_filter = {
        'weekday': Q(registration_date__gte=datetime.now() - timedelta(days=1)),
        'weekends': Q(registration_date__gte=datetime.now() - timedelta(days=3)),
    }
    num_days = datetime.now().weekday()
    final_query = base_query & type_days_filter[get_type_day(num_days)]
    new_users = User.objects.filter(final_query)
    count_new_users = new_users.count()

    if count_new_users:
        base_notifications_data = Notifications.get_basiс_data_notification(
            type_notification=Notifications.TYPE_NEW_USERS,
            count_new_users=count_new_users
        )
        recipients = User.objects.filter(
            staff__position=StaffUser.POSITION_ADMINISTRATOR,
            is_account_confirmation=True,
            staff__receiver=True
        )
        notifications = Notifications(
            ** base_notifications_data
        )
        notifications.save()
        notifications.recipients.set(recipients)

        notifications.create_send_email()  # Отправка нотификации в отправку

    return count_new_users


def get_type_day(num_day):
    if 5 <= num_day <= 6:
        return 'weekends'
    return 'weekday'












