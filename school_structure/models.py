from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count
from mptt.models import MPTTModel, TreeForeignKey

__all__ = ('School', 'EducationalСlass', 'DirectionScience', \
           'Topic', 'Subject', 'TimeTable', 'ScoreStudent')


class SchollManager(models.Manager):
    """Менеджер модели школы"""
    def all_with_counts(self):
        """Метод получения кол-ва элементов в структуре школы"""
        return School.objects.only('id').annotate(count_directions=Count('directions', distinct=True)) \
            .annotate(count_students=Count('classes__students', distinct=True)) \
            .annotate(count_classes=Count('classes', distinct=True)) \
            .annotate(count_subjects=Count('directions__subjects', distinct=True))


class School(models.Model):
    """Модель школы"""
    name = models.CharField(max_length=300, verbose_name='Название школы')
    addres = models.CharField(max_length=300, verbose_name='Адресс школы')
    email = models.EmailField(max_length=100, verbose_name='Электронный адрес')
    objects = SchollManager()

    class Meta:
        verbose_name = 'Образовательная организация'
        verbose_name = 'Образовательная организации'

    @property
    def director(self):
        """Директор школы"""
        from users.models import StaffUser
        director = StaffUser.objects.filter(position=StaffUser.POSITION_DIRECTOR, school_id=self.id).first()
        return director

    @property
    def administrations(self):
        """Администрация школы"""
        from users.models import StaffUser
        admins = StaffUser.objects.filter(
            position=StaffUser.POSITION_ADMINISTRATOR,
            school_id=self.id)

        return admins

    def __str__(self):
        return self.name


class EducationalСlass(models.Model):
    """Модель учебного класса"""
    name = models.CharField(max_length=300, verbose_name='Название класса',
                            unique=True, error_messages={'unique': "Класс с таким именем уже существует"}
                            )
    school = models.ForeignKey(School, verbose_name='Школа', related_name='classes', on_delete=models.CASCADE)
    timetable = models.ManyToManyField('TimeTable', verbose_name='Расписание', related_name='classes',
                                       blank=True, null=True
                                       )

    class Meta:
        verbose_name = 'Образовательный класс'
        verbose_name = 'Образовательные классы'

    @property
    def count_students(self):
        return self.students.count()

    def __str__(self):
        return self.name


class DirectionScience(models.Model):
    """Модель учебного направления"""
    name = models.CharField(max_length=300, verbose_name='Название направления')
    school = models.ForeignKey(School, verbose_name='Школа', related_name='directions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учебное направление'
        verbose_name = 'Учебные направления'

    @property
    def count_programs(self):
        return self.subjects.count()

    def __str__(self):
        return self.name


class Topic(MPTTModel):
    """Модель темы занятий"""
    name = models.CharField(max_length=300, verbose_name='Название темы')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тема занятия'
        verbose_name = 'Темы занятий'

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Модель Учебного предмета"""
    name = models.CharField(max_length=300, verbose_name='Название Предмета')
    topic = models.ManyToManyField(Topic, verbose_name='Тема занятий', null=True, blank=True)
    direction_science = models.ForeignKey(DirectionScience, verbose_name='Учебное направление', related_name='subjects',
                                          on_delete=models.SET_NULL, blank=True, null=True
                                          )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name = 'Предметы'

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    """Модель расписания занятий"""
    DAYS_TYPES = ((1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'),
                  (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресенье')
                  )
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE, blank=True)
    topic = models.ManyToManyField(Topic, verbose_name='Темы занятий', blank=True, null=True)
    day = models.PositiveSmallIntegerField(verbose_name='День недели', choices=DAYS_TYPES)
    start_time = models.TimeField(verbose_name='Начало работы', blank=True, null=True)
    end_time = models.TimeField(verbose_name='Конец работы', blank=True, null=True)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    # def __str__(self):
    #     return f'{self.day}-{self.subject.name}'


class ScoreStudent(models.Model):
    """Модель оценок студента"""
    value = models.PositiveSmallIntegerField(verbose_name='Оценка',
                                             validators=[MinValueValidator(0), MaxValueValidator(5)]
                                             )
    subject = models.ForeignKey(Subject, verbose_name='Предмет', related_name='scores', on_delete=models.CASCADE,
                                blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name='Тема занятий', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.value}'
