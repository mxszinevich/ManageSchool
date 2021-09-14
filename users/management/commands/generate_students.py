from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User,Student

class Command(BaseCommand):
    help = 'Моя первая команда'
    COUNT_FAKE_USERS=40
    COUNT_FAKE_CLASSES=10

    def handle(self, *args, **options):
        fake = Faker(locale="ru_RU")

        for _ in range(Command.COUNT_FAKE_USERS):
            fake_users_data={
            'last_name':fake.last_name(),
            'first_name':fake.first_name(),
            'middle_name':fake.middle_name(),
            'email':fake.email(),
            'date_of_birth':fake.date_of_birth(),
            'phone_number':fake.phone_number(),
            'password':'user'
            }

            Student.objects.create(user=User.objects.create(**fake_users_data))




