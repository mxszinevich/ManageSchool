from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from users.models import StaffUser, Student


class SchoolStructure(models.Model):
    """Образовательное учреждение"""
    name=models.CharField(max_length=300,verbose_name='Название школы')
    slug=models.SlugField(max_length=300,verbose_name='url школы')
    directions_science=models.ManyToManyField('DirectionScience',verbose_name='Направления обучения',blank=True,null=True)
    addres=models.CharField(max_length=300,verbose_name='Адресс школы')
    email=models.EmailField(max_length=100,verbose_name='Электронный адрес')

    class Meta:
        verbose_name='Образовательная организация'
        verbose_name='Образовательные организации'

    def __str__(self):
        return self.name


class EducationalСlass(models.Model):
    """Учебные классы образовательного учреждения"""
    name = models.CharField(max_length=300, verbose_name='Название класса')
    slug = models.SlugField(max_length=300, verbose_name='url класса')
    school=models.ForeignKey(SchoolStructure,verbose_name='Школа',related_name='classes',on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, verbose_name='Учащиеся',blank=True,related_name='classes')


    class Meta:
        verbose_name='Образовательный класс'
        verbose_name='Образовательные классы'

    def __str__(self):
        return self.name

class DirectionScience(models.Model):
    """Учебные направления образовательного учреждения"""
    name = models.CharField(max_length=300, verbose_name='Название направления')
    slug = models.SlugField(max_length=300, verbose_name='url направления')
    school = models.ForeignKey(SchoolStructure, verbose_name='Школа', related_name='directions', on_delete=models.CASCADE)

    class Meta:
        verbose_name='Учебное направление'
        verbose_name='Учебные направления'

    def __str__(self):
        return self.name

class Topic(MPTTModel):
    """Тема занятия"""
    name = models.CharField(max_length=300, verbose_name='Название темы')
    parent=TreeForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Тема занятия'
        verbose_name='Темы занятий'

    def __str__(self):
        return self.name

class Subject(models.Model):
    """Учебный предмет"""
    name = models.CharField(max_length=300, verbose_name='Название Предмета')
    topic=models.ManyToManyField(Topic,verbose_name='Тема занятий',null=True,blank=True)

    # @TODO можно дополнить дополнительными полями

    class Meta:
        verbose_name = 'Предмет'
        verbose_name = 'Предметы'

    def __str__(self):
        return self.name

class TimeTable(models.Model):
    """Расписание занятий"""
    subject=models.ForeignKey(Subject,verbose_name='Предмет',on_delete=models.CASCADE)
    topic=models.ManyToManyField(Topic,verbose_name='Темы занятий',blank=True,null=True)
    educational_class=models.ManyToManyField(EducationalСlass,verbose_name='Образовательные классы',related_name='timetable',blank=True,null=True)
    teacher=models.ManyToManyField(StaffUser,verbose_name='Учитель(я)',related_name='timetable',blank=True,null=True)
    day=models.DateField(verbose_name='День занятий')
    start_time=models.TimeField(verbose_name='Начало занятий')
    end_time=models.TimeField(verbose_name='Конец занятий')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name = 'Расписание'

    def __str__(self):
        return f'{self.day}-{self.subject.name}-{self.teacher}'











