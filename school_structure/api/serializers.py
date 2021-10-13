from rest_framework import serializers
from rest_framework.exceptions import APIException

from school_structure.models import *
from users.api.serializers import StudentSerializer, StaffUserSerializer


class DirectionScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionScience
        fields = ('id', 'name', 'count_programs')
        read_only_fields = ('count_programs',)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'direction_science')

    def to_representation(self, instance):
        representation = super(SubjectSerializer, self).to_representation(instance)
        representation['direction_science'] = {
            'id': instance.direction_science_id,
            'name': instance.direction_science.name
        }
        return representation


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


class EducationalСlassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = EducationalСlass
        fields = ('id', 'name', 'school', 'count_students', 'students')

    def validate_name(self, value):
        # @TODO добавить проверки
        if len(value.split()) > 1:
            raise serializers.ValidationError('Название класса должно быть указано без пробела')
        return value


class ListEducationalСlassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = EducationalСlass
        fields = ('id', 'name', 'count_students', 'school')
        read_only_fields = ('name', 'count_students')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'parent_id')


class TimeTableUserSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True, required=False)
    end_time = serializers.TimeField(required=True)

    # day = DAYserializer(read_only=True)
    # day_id = DAYserializer(write_only=True)
    class Meta:
        model = TimeTable
        fields = ('id', 'day', 'topic', 'subject', 'end_time', 'classes')

    def to_representation(self, instance):  # Сериализатор
        representation = super(TimeTableUserSerializer, self).to_representation(instance)
        if self.context['request'].method == 'GET':
            representation['subject'] = {'id': representation['subject'], 'name': instance.subject.name}
            representation['day'] = {'id': representation['day'], 'name': instance.get_day_display()}
        return representation


class TimeTableSerializer(TimeTableUserSerializer):
    classes = ListEducationalСlassSerializer(many=True)

    # @ TODO добавить расписание класса
    # @TODO Проверить метод create
    # @ TODO Проверка на существование timetable
    def create(self, validated_data):
        ed_classes = validated_data.pop('classes', None)
        timetable = TimeTable.objects.create(**validated_data)
        for ed_class_info in ed_classes:
            id_ed_class = ed_class_info.get('id')
            school = ed_class_info.get('school')
            if id_ed_class:
                try:
                    ed_class = EducationalСlass.objects.get(id=id_ed_class, school_id=school.id)
                except:
                    raise APIException('Класса с id не существует')
            ed_class.timetable.add(timetable)
            ed_class.save()
        return timetable


class ScoreStudentSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    subject = serializers.CharField()
    date = serializers.DateField()
    topic = serializers.CharField()
