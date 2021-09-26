from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from school_structure.api.serializers import TimeTableSerializer
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


    def get_timetable(self, *args, **kwargs):
        # @ TODO Некорректно
        ed_class = EducationalСlass.objects.prefetch_related('timetable').get(students__id=kwargs['pk'])
        timetable = ed_class.timetable.all()
        result = []

        if timetable:
            serializer = TimeTableSerializer(timetable, many=True)
            result= serializer.data

        return Response(result)



    # def update(self, request, *args, **kwargs):
    #     update_student = get_object_or_404(Student.objects.all(), pk=kwargs['pk'])
    #     serializer = StudentSerializer(instance=update_student, data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         update_student = serializer.save()
    #     return  Response({'success':f'{update_student} updated'})














