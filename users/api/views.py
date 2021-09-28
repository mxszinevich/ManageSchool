from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from school_structure.api.serializers import TimeTableUserSerializer, TimeTableSerializer
from school_structure.models import TimeTable, EducationalСlass
from users.models import StaffUser, Student, User
from .serializers import StaffUserSerializer, StudentSerializer


class StudentsResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StaffListView(viewsets.ModelViewSet):

    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer

class StudentsListView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentsResultsSetPagination

    # serializer_classes_by_action = {
    #     'list': AuthorTrackSerializer
    # }
    # @TODO исправить получение расписания
    @action(methods=['GET'], detail=False, name='get_timetable')
    def get_timetable(self, *args, **kwargs):
        timetable = TimeTable.objects.filter(classes__students__id=kwargs['pk'])

        result = []
        if timetable:
            serializer = TimeTableSerializer(timetable, many=True)
            result= serializer.data

        return Response(result)















