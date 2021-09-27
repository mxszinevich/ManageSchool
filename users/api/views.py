from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from school_structure.api.serializers import  TimeTableUserSerializer
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

    # @TODO получение расписание у Students. Подключение к маршрушизатору
    # @TODO декораторы: actions, api_view
    @action(methods=['GET'], detail=False)
    def get_timetable(self, *args, **kwargs):
        ed_class = EducationalСlass.objects.prefetch_related('timetable').get(students__id=kwargs['pk'])
        timetable = ed_class.timetable.all()

        result = []
        if timetable:
            serializer = TimeTableUserSerializer(timetable, many=True)
            result= serializer.data

        return Response(result)

    # @TODO Как улучшить обновление
    def update(self, request, *args, **kwargs):
        update_student = get_object_or_404(Student.objects.all(), pk=kwargs['pk'])

        if request.data['personal_info']['email'] == update_student.user.email:
            del request.data['personal_info']['email']

        if request.data['personal_info']['phone_number'] == update_student.user.phone_number:
            del request.data['personal_info']['phone_number']

        serializer = StudentSerializer(instance=update_student, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            update_student = serializer.save()

        return  Response({'success':f'{update_student} updated'})














