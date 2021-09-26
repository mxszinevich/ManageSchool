from rest_framework import serializers
from school_structure.models import Subject
from users.models import User, StaffUser, Student, ParentsStudent


class UserSerializer(serializers.ModelSerializer):
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
    #school=SchoolSerializer()
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
    personal_info = UserSerializer(source='user', required=False)
    educational_class = serializers.CharField()
    parents = ParentsStudentSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = ('id', 'educational_class', 'personal_info', 'parents')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['educational_class'] = {'id': instance.educational_class.id, 'name': instance.educational_class.name}
        return representation













