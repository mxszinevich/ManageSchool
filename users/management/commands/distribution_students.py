from django.core.management.base import BaseCommand
from users.models import User,Student
from school_structure.models import EducationalСlass
from faker import Faker
import random

class Command(BaseCommand):

    help = 'Распределение студентов по классам'
    MAX_COUNT_STUDENTS = 30
    MIN_COUNT_STUDENTS = 20
    def handle(self, *args, **options):
        for educational_class in EducationalСlass.objects.all():
            count_students = random.randint(Command.MIN_COUNT_STUDENTS, Command.MAX_COUNT_STUDENTS)
            students = Student.objects.select_related('educational_class').filter(educational_class=None)[:count_students]

            for student in students:
                student.educational_class = educational_class
                student.save(update_fields=['educational_class'])

            # Student.objects.bulk_update(students, ['educational_class'])











