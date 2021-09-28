from rest_framework import serializers
from school_structure.models import *
from users.api.serializers import StudentSerializer, StaffUserSerializer


class DirectionScienceSerializer(serializers.ModelSerializer):
    count_programs = serializers.SerializerMethodField()

    class Meta:
        model = DirectionScience
        fields = ('id','name','count_programs')
        read_only_fields = ('id','count_programs',)

    def get_count_programs(self, instance):
        return instance.subjects.count()

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'name', 'direction_science')
        read_only_fields = ('id', )

    def to_representation(self, instance):
        representation = super(SubjectSerializer, self).to_representation(instance)
        representation['direction_science'] = {'id': instance.direction_science_id
            , 'name': instance.direction_science.name}
        return  representation


class SchoolSerializer(serializers.ModelSerializer):
    # @TODO: дописать руководство
    direction_science = DirectionScienceSerializer(many=True, source='directions')
    staff = StaffUserSerializer(many=True)
    count_directions = serializers.IntegerField()
    count_students = serializers.IntegerField()
    count_classes = serializers.IntegerField()
    count_subjects = serializers.IntegerField()

    class Meta:
        model = School
        fields = ('id', 'name', 'addres', 'email',
                  'count_directions', 'count_students', 'count_classes', 'count_subjects',
                  'direction_science', 'staff')
        read_only_fields = ('id',)



class EducationalСlassSerializer(serializers.ModelSerializer):
    count_students = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, required=False)

    class Meta:
        model = EducationalСlass
        fields = ('id', 'name', 'school', 'count_students', 'students')
        read_only_fields = ('id', 'students')

    def validate_name(self, value):
        # @TODO добавить проверки
        if len(value.split())>1:
            raise serializers.ValidationError('Название класса должно быть указано без пробела')
        return value

    def get_count_students(self, instance):
        return instance.students.count()


class ListEducationalСlassSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationalСlass
        fields = ('id', 'name', 'school')
        read_only_fields = ('id',)

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'parent_id')


class TimeTableUserSerializer(serializers.ModelSerializer):
    #subject_id = serializers.IntegerField(write_only=True)  # @TODO Разные поля для POST и GET запроса
    topic = TopicSerializer(many=True, required=False)
    end_time = serializers.TimeField(required=True)

    class Meta:
        model = TimeTable
        fields = ('__all__')


class TimeTableUserSerializer2(TimeTableUserSerializer):
    subject = SubjectSerializer(read_only=True)


class TimeTableSerializer(TimeTableUserSerializer):
    classes = ListEducationalСlassSerializer(many=True, required=False)





