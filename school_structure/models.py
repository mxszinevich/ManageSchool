from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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


class Subject(models.Model):
    """Учебный предмет"""
    name = models.CharField(max_length=300, verbose_name='Название Предмета')


class Topic(MPTTModel):
    """Тема занятия"""
    name = models.CharField(max_length=300, verbose_name='Название темы')
    parent=TreeForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,verbose_name='Предмет',related_name='lessons_topic',blank=True,null=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.name



class Lession(models.Model):
    """Учебное занятие"""







