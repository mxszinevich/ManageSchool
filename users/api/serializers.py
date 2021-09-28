from rest_framework import serializers, exceptions
from school_structure.models import Subject
from users.models import User, StaffUser, Student, ParentsStudent
from school_structure.models import EducationalСlass


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'middle_name', 'email', 'image',
            'date_of_birth', 'phone_number'
        )
        read_only = ('password',)
        ref_name ='ProjectBaseUser'

class StaffUserSerializer(serializers.ModelSerializer):
    base_info = UserSerializer(source = 'user')
    class Meta:
        model = StaffUser
        fields = ('base_info',)


class ParentsStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentsStudent
        fields = ('__all__')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('__all__')

class StudentSerializer(serializers.ModelSerializer):
    personal_info = UserSerializer(source='user')
    educational_class= serializers.CharField()
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
            EducationalСlass.objects.only('id').get(id=int(validated_data['educational_class']))
        except Student.DoesNotExist:
            raise exceptions.APIException(detail='Student DoesNotExist')
        except EducationalСlass.DoesNotExist:
            raise exceptions.APIException(detail='EducationalСlass DoesNotExist')
        except ValueError:
            raise exceptions.APIException(detail='educational_class not int')

        student.educational_class_id = int(validated_data['educational_class'])
        student.save(update_fields=['educational_class_id'])
        return student
















