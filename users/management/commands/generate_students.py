from django.core.management.base import BaseCommand
from users.models import User,Student
from faker import Faker

class Command(BaseCommand):

    help = 'Генерация студентов'
    COUNT_FAKE_USERS = 360

    def handle(self, *args, **options):
        students = [Student(user=User.objects.create_user(**self.get_fake_user())) for _ in range(Command.COUNT_FAKE_USERS)]
        Student.objects.bulk_create(students)

    def get_fake_user(self):
        fake = Faker(locale="ru_RU")
        name = fake.name().split()
        last_name, first_name, middle_name = fake.name().split()[:3]
        return {
                'last_name': last_name,
                'first_name': first_name,
                'middle_name': middle_name,
                'email': fake.email(),
                'date_of_birth': fake.date_of_birth(),
                'phone_number': fake.phone_number(),
                'password': 'user'
                }




