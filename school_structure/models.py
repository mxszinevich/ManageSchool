from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count
from mptt.models import MPTTModel, TreeForeignKey

__all__ = ('School', 'EducationalСlass', 'DirectionScience', \
           'Topic', 'Subject', 'TimeTable', 'ScoreStudent')

class SchollManager(models.Manager):

    def all_with_counts(self):
        return School.objects.only('id').annotate(count_directions=Count('directions', distinct=True))\
                .annotate(count_students=Count('classes__students', distinct=True))\
                .annotate(count_classes=Count('classes', distinct=True) )\
                .annotate(count_subjects=Count('directions__subjects', distinct=True) )

class School(models.Model):
    """Образовательное учреждение"""
    name = models.CharField(max_length=300, verbose_name='Название школы')
    addres = models.CharField(max_length=300, verbose_name='Адресс школы')
    email = models.EmailField(max_length=100, verbose_name='Электронный адрес')

    objects = SchollManager()

    class Meta:
        verbose_name = 'Образовательная организация'
        verbose_name = 'Образовательная организации'

    def __str__(self):
        return self.name


class EducationalСlass(models.Model):
    """Учебные классы образовательного учреждения"""
    name = models.CharField(
        max_length=300,
        verbose_name='Название класса',
        unique=True,
        error_messages={'unique': "Класс с таким именем уже существует"},
    )
    school = models.ForeignKey(School, verbose_name='Школа', related_name='classes', on_delete=models.CASCADE)
    timetable = models.ManyToManyField('TimeTable', verbose_name='Расписание', related_name='classes', blank=True, null=True)

    class Meta:
        verbose_name = 'Образовательный класс'
        verbose_name = 'Образовательные классы'

    @property
    def count_students(self):
        return self.students.count()

    def __str__(self):
        return self.name


class DirectionScience(models.Model):
    """Учебные направления образовательного учреждения"""
    name = models.CharField(max_length=300, verbose_name='Название направления')
    school = models.ForeignKey(School, verbose_name='Школа', related_name='directions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учебное направление'
        verbose_name = 'Учебные направления'

    def __str__(self):
        return self.name


class Topic(MPTTModel):
    """Тема занятия"""
    name = models.CharField(max_length=300, verbose_name='Название темы')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тема занятия'
        verbose_name = 'Темы занятий'

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Учебный предмет"""
    name = models.CharField(max_length=300, verbose_name='Название Предмета')
    topic = models.ManyToManyField(Topic, verbose_name='Тема занятий', null=True, blank=True)
    direction_science = models.ForeignKey(
        DirectionScience,
        verbose_name='Учебное направление',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subjects'
    )

    # @TODO можно дополнить дополнительными полями

    class Meta:
        verbose_name = 'Предмет'
        verbose_name = 'Предметы'

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    """Расписание занятий"""
    DAYS_TYPES = (
        (1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'),
        (7, 'Воскресенье')
    )
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE, blank=True)
    topic = models.ManyToManyField(Topic, verbose_name='Темы занятий', blank=True, null=True)
    day = models.PositiveSmallIntegerField(verbose_name='День недели', choices=DAYS_TYPES)
    start_time = models.TimeField(verbose_name='Начало работы')
    end_time = models.TimeField(verbose_name='Конец работы', blank=True)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name = 'Расписание'

    # def __str__(self):
    #     return f'{self.day}-{self.subject.name}'


class ScoreStudent(models.Model):
    value = models.PositiveSmallIntegerField(
        verbose_name='Оценка', validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    subject = models.ForeignKey(Subject, verbose_name='Предмет', related_name='scores', on_delete=models.CASCADE, blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name='Тема занятий', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(verbose_name='Дата',)

    class Meta:
        verbose_name = 'Оценка'

    def __str__(self):
        return f'{self.value}'
