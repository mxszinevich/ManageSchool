from django.conf import settings
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

import users.utils
from school_structure.models import School, TimeTable, EducationalСlass, ScoreStudent


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **required_fields):
        if not email:
            raise ValueError('Необходимо указать email')

        user = self.model(
            email=self.normalize_email(email),
            **required_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **required_fields):
        if not email:
            raise ValueError('Необходимо указать email')
        user = self.create_user(
            email,
            password=password,
            **required_fields
        )
        user.is_admin = True
        user.is_account_confirmation = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Кастомный пользователь"""
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', max_length=255, unique=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True,
                              upload_to=users.utils.create_path_media_user)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone_number = models.CharField(verbose_name='Телефонный номер', validators=[users.utils.phone_validation],
                                    max_length=30, blank=True, unique=True)
    extra_info = models.JSONField(verbose_name='Дополнительная информация', blank=True, null=True)
    is_account_confirmation = models.BooleanField(verbose_name='Подтверждение аккаунта в системе', default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def short_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class StaffUser(models.Model):
    """Кастомная модель пользователя"""
    POSITION_TEACHER = 1
    POSITION_MANAGER_DIRECTION = 2
    POSITION_ADMINISTRATOR = 3
    POSITION_DIRECTOR = 4

    POSITION_STAFF_CHOISES = (
        (POSITION_TEACHER, 'Учитель'),
        (POSITION_MANAGER_DIRECTION, 'Руководитель направления'),
        (POSITION_ADMINISTRATOR, 'Администратор'),
        (POSITION_DIRECTOR, 'Директор'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff')
    position = models.PositiveSmallIntegerField(verbose_name='Должность', choices=POSITION_STAFF_CHOISES)
    school = models.ForeignKey(School,
                               verbose_name='Образовательная организация', on_delete=models.CASCADE,
                               blank=True, null=True, related_name='staff')
    timetable = models.ManyToManyField(TimeTable, verbose_name='График работы',
                                       related_name='staff_users', blank=True, )

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = 'Сотрудник'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super(StaffUser, self).delete(using=None, keep_parents=False)


class Student(models.Model):
    """Класс студента"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    start_learning = models.DateField(verbose_name='Начало обучения', blank=True, auto_now=True)
    end_learning = models.DateField(verbose_name='Конец обучения', blank=True, null=True)
    parents = models.ManyToManyField('users.ParentsStudent', verbose_name='Родители', blank=True, null=True)
    educational_class = models.ForeignKey(EducationalСlass,
                                          verbose_name='Образовательный класс',
                                          on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    score = models.ManyToManyField(ScoreStudent, verbose_name='оценки', blank=True,
                                   related_name='students')

    class Meta:
        verbose_name = 'Учащийся'

    def __str__(self):
        return self.user.full_name

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super(Student, self).delete(using=None, keep_parents=False)


class ParentsStudent(models.Model):
    """Класс родителей студента"""
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    phone_number = models.CharField(verbose_name='Телефонный номер', validators=[users.utils.phone_validation],
                                    max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name = 'Родители'
        unique_together = ('first_name', 'last_name', 'phone_number')
