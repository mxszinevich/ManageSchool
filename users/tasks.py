import pandas
from config import settings
from config.celery import celery_app
from users.models import User, Student
from django.core.mail import send_mail

from config import settings


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
    base_model = Student
    table_reports = [base_model, User]
    template = TemplateReports(*table_reports)
    data_frame = {}
    table_data = Student.objects.select_related('user').order_by('id').values()
    for column_name in template.fields_names:
        data_frame[column_name] = [row_data.get(column_name) for row_data in table_data]
        data_frame[column_name] = [User.objects.filter(id=row_data.get('user_id')).values().first().get(column_name) for row_data in table_data]
    pandas.DataFrame(data_frame).to_excel(settings.MEDIA_ROOT + '/reports/reports.xlsx')

@celery_app.task
def cancel_registration():
    print('отправка')
    send_mail("cron", "cron", settings.EMAIL_HOST_USER, ['maksim.zinevich@bk.ru'])

    # * * * * * /usr/bin/python /ome/maksim/Рабочий стол/DjangoLearn/ManageSchool cancel_registrat