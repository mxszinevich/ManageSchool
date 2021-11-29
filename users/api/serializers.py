from django.db import transaction, IntegrityError
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from djoser.conf import settings as djoser_settings

from notifications.models import Notifications
from users.models import User, StaffUser, Student, ParentsStudent


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для GET, POST, DELETE запросов"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'middle_name', 'email', 'image',
                  'date_of_birth', 'phone_number',
                  'password', 'is_account_confirmation',
                  )
        extra_kwargs = {
            'password': {'write_only': True},
            # 'is_account_confirmation': {'write_only': True},
        }
        ref_name = 'ProjectBaseUser'  # Необходимо для djoser


class UpdateUserSerializer(UserSerializer):
    """Сериализатор пользователя для PUT запросов"""
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField()
    is_account_confirmation = serializers.BooleanField(write_only=True, required=False)


class ReadAllUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для просмотра неавторизованными пользователями"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'image',)


class StaffUserSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника для GET, POST, DELETE запросов"""
    personal_info = UserSerializer(source='user')

    class Meta:
        model = StaffUser
        fields = ('id', 'personal_info', 'position', 'school')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user'))
        staff = StaffUser.objects.create(user=user, **validated_data)
        return staff


class UpdateStaffUserSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника для Update запросов"""
    personal_info = UpdateUserSerializer(source='user')

    class Meta:
        model = StaffUser
        fields = ('id', 'personal_info', 'position', 'school')

    def update(self, instance, validated_data):
        """"Метод обновления персонала"""
        new_user_password = validated_data['user'].pop('password', None)

        exists_unique_fields = []
        if validated_data['user']['email'] != instance.user.email:
            if User.objects.filter(email=validated_data['user']['email']):
                exists_unique_fields.append({'email': 'Пользователь с таким email уже существует'})
        if validated_data['user']['phone_number'] != instance.user.phone_number:
            if User.objects.filter(phone_number=validated_data['user']['phone_number']):
                exists_unique_fields.append({'phone_number': 'Пользователь с таким phone_number уже существует'})
        if exists_unique_fields:
            raise ValidationError(exists_unique_fields)

        is_account_confirmation = validated_data['user'].get('is_account_confirmation')
        if is_account_confirmation and is_account_confirmation != instance.user.is_account_confirmation:
            # Создаем уведомление
            email = Notifications(theme='Изменение статуса', body='Статус изменен')
            #email.save()
            #email.recipients.add(instance.user)
            #email.send_email()  # Отправляем уведомление

        User.objects.filter(id=instance.user_id).update(**validated_data.pop('user'))

        if new_user_password:
            user = User.objects.get(id=instance.user_id)
            user.set_password(new_user_password)
            user.save(update_fields=['password'])

        StaffUser.objects.filter(id=instance.id).update(**validated_data)
        staff_user = StaffUser.objects.get(id=instance.id)
        return staff_user


class ReadAllStaffUserSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника для просмотра неавторизованным пользователям"""
    personal_info = ReadAllUserSerializer(source='user')

    class Meta:
        model = StaffUser
        fields = ('personal_info', 'position', 'school')


class AdministrationSchoolSerializer(serializers.Serializer):
    """Сериализатор администрации школы"""
    name = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')


class ParentsStudentSerializer(serializers.ModelSerializer):
    """Сериализатор родителей"""

    class Meta:
        model = ParentsStudent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор студента для GET, POST, запросов"""
    personal_info = UserSerializer(source='user')
    # educational_class = serializers.IntegerField(source='educational_class_id')
    parents = ParentsStudentSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = ('id', 'educational_class', 'personal_info', 'parents')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            representation['educational_class'] = {
                'id': instance.educational_class_id,
                'name': instance.educational_class.name
            }
        except AttributeError:
            pass

        return representation

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user'))
        try:
            parents = validated_data.pop('parents', None)
            student = Student.objects.create(user=user, **validated_data)
            if parents:
                student.parents.set(parents)
                student.save()
        except Exception as ex:
            user.delete()
            raise exceptions.APIException(detail='Ошибка создания пользователя')
        return student


class UpdateStudentSerializer(UpdateStaffUserSerializer):
    """Сериализатор студента для PUT запросов"""
    educational_class = serializers.IntegerField(source='educational_class_id')
    parents = ParentsStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'educational_class', 'personal_info', 'parents')

    def update(self, instance, validated_data):
        new_password_user = validated_data['user'].pop('password', None)
        User.objects.filter(id=instance.user_id).update(**validated_data.pop('user'))

        if new_password_user:
            user = User.objects.get(id=instance.user_id)
            user.set_password(new_password_user)
            user.save(update_fields=['password'])

        parents = validated_data.pop('parents', None)
        Student.objects.filter(id=instance.id).update(**validated_data)
        student = Student.objects.get(id=instance.id)
        if parents:
            student.parents.set(parents)
        return student


class RegistrationStaffUserSerializer(UserCreateSerializer):
    """Сериализатор регистрации сотрудников школы с подтверждением email(djoser)"""
    personal_info = UserSerializer(source='user')

    class Meta:
        model = StaffUser
        fields = ('personal_info', 'position', 'school')

    def validate(self, attrs):
        return super(UserCreateSerializer, self).validate(attrs)

    # @TODO Зачем perform_create
    def create_staffuser(self, validated_data):
        # @ TODO transaction
        # https://github.com/sunscrapers/djoser/blob/master/djoser/serializers.py
        with transaction.atomic():
            user = User.objects.create_user(**validated_data.pop('user'))
            staff = StaffUser.objects.create(user=user, **validated_data)
            if djoser_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user, staff

    def create(self, validated_data):
        try:
            user, staff = self.create_staffuser(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return staff


class RegistrationStudentUserSerializer(UserCreateSerializer):
    """Сериализатор регистрации студентов школы с подтверждением email(djoser)"""
    personal_info = UserSerializer(source='user')
    parents = ParentsStudentSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Student
        fields = ('id', 'educational_class', 'personal_info', 'parents')
        extra_kwargs = {
            'educational_class': {'write_only': 'True'},
        }

    def validate(self, attrs):
        return super(UserCreateSerializer, self).validate(attrs)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data.pop('user'))
                parents = validated_data.pop('parents', None)
                student = Student.objects.create(user=user, **validated_data)
                if parents:
                    student.parents.set(parents)
                    student.save()
                if djoser_settings.SEND_ACTIVATION_EMAIL:
                    user.is_active = False
                    user.save(update_fields=["is_active"])
        except Exception as ex:
            # user.delete() @TODO нужно ли это если есть  транзакция ?
            raise exceptions.APIException(detail='Ошибка создания пользователя')
        return student
