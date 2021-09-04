from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from .users_validators import _phone_validation

class StaffUserManager(BaseUserManager):

    def create_user(self, email,password=None, **required_fields):
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

        print(required_fields)
        user = self.create_user(
            email,
            password=password,
            **required_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def create_path_media_user(instance, filename):

    return f'Пользователи/{instance.position}/{instance.full_name}/Профиль_{instance.last_name}_.{filename.split(".")[-1]}'

class StaffUser(AbstractBaseUser):
    """Кастомная модель пользователя"""
    # @TODO добавить предметы

    POSITION_TEACHER=1
    POSITION_MANAGER_DIRECTION=2
    POSITION_ADMINISTRATOR=3
    POSITION_DIRECTOR=4

    POSITION_STAFF_CHOISES=(
        (POSITION_TEACHER,'Учитель'),
        (POSITION_MANAGER_DIRECTION,'Руководитель направления'),
        (POSITION_ADMINISTRATOR,'Администратор'),
        (POSITION_DIRECTOR,'Директор'),
    )

    first_name=models.CharField(verbose_name='Имя',max_length=255)
    last_name=models.CharField(verbose_name='Фамилия',max_length=255)
    middle_name=models.CharField(verbose_name='Отчество',max_length=255)
    email = models.EmailField(verbose_name='Электронная почта',max_length=255, unique=True,)
    image=models.ImageField(verbose_name='Изображение',blank=True,upload_to=create_path_media_user)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone_number = models.CharField(verbose_name='Телефонный номер',validators=[_phone_validation], max_length=17, blank=True)
    position=models.PositiveSmallIntegerField(verbose_name='Должность',choices=POSITION_STAFF_CHOISES)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = StaffUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','phone_number','position','first_name','last_name','middle_name']

    def __str__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'



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



