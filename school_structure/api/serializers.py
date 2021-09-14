from rest_framework import serializers
from school_structure.models import *
from users.api.serializers import StudentSerializer,StaffUserSerializer

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Subject
        fields=('id','name',)
        read_only=('id',)

class DirectionScienceSerializer(serializers.ModelSerializer):
    count_programs=serializers.SerializerMethodField()

    class Meta:
        model=DirectionScience
        fields=('id','name','count_programs')
        read_only = ('id','count_programs',)

    def get_count_programs(self,instance):
        return instance.subjects.count()


class SchoolSerializer(serializers.ModelSerializer):
    # @TODO: дописать руководство
    direction_science=DirectionScienceSerializer(many=True, source='directions')
    count_direction_science=serializers.SerializerMethodField()
    count_subjects=serializers.SerializerMethodField()
    count_classes=serializers.SerializerMethodField()
    count_students=serializers.SerializerMethodField()
    staff=StaffUserSerializer(many=True)
    class Meta:
        model=School
        fields = ('id','name','addres','email',
                  'direction_science','count_subjects','count_classes',
                  'count_students','count_direction_science','staff')
        read_only = ('id',)

    def get_count_subjects(self,instance):
        return sum([direction.subjects.count() for direction in instance.directions.all()])

    def get_count_classes(self,instance):
        return instance.classes.count()

    def get_count_students(self,instance):
        return sum([ed_class.students.count() for ed_class in instance.classes.all()])

    def get_count_direction_science(self,instance):
        return instance.directions.count()


class EducationalСlassSerializer(serializers.ModelSerializer):
    students=StudentSerializer(many=True)
    class Meta:
        model=EducationalСlass
        fields=('id','name','students')

