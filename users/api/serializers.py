from rest_framework import serializers, exceptions
from rest_framework.decorators import action

from school_structure.models import Subject
from users.models import User, StaffUser, Student, ParentsStudent
from school_structure.models import EducationalСlass


class UserSerializer(serializers.ModelSerializer):
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
        ref_name = 'ProjectBaseUser'

class UpdateUserSerializer(serializers.Serializer):
    is_account_confirmation = serializers.BooleanField()


class StaffUserSerializer(serializers.ModelSerializer):
    personal_info = UpdateUserSerializer(source='user')

    class Meta:
        model = StaffUser
        fields = ('id', 'personal_info', 'position', 'school')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user')) # @TODO create ?
        staff = StaffUser.objects.create(user=user, **validated_data)
        return staff

    def update(self, instance, validated_data):
        user = User.objects.filter(id=instance.user_id).update(**validated_data.pop('user'))
        staff_user = StaffUser.objects.get(id=instance.id)
        staff_user.position = validated_data['position']
        staff_user.school = validated_data['school']
        staff_user.save(update_fields=[*validated_data])
        return staff_user





class ParentsStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentsStudent
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    personal_info = UserSerializer(source='user')
    educational_class = serializers.CharField()
    parents = ParentsStudentSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = ('id', 'educational_class', 'personal_info', 'parents')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['educational_class'] = {
            'id': instance.educational_class.id,
            'name': instance.educational_class.name
        }
        return representation

    def update(self, instance, validated_data):
        User.objects.filter(id=instance.user_id).update(**validated_data['user'])

        try:
            student = Student.objects.get(id=instance.id)
            educational_class = EducationalСlass.objects.only('id').get(id=int(validated_data['educational_class']))
        except Student.DoesNotExist:
            raise exceptions.APIException(detail='Student DoesNotExist')
        except EducationalСlass.DoesNotExist:
            raise exceptions.APIException(detail='EducationalСlass DoesNotExist')
        except ValueError:
            raise exceptions.APIException(detail='EducationalClass not int')

        student.educational_class_id = educational_class.id
        student.save(update_fields=['educational_class_id'])

        return student
