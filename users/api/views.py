from rest_framework import viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from school_structure.api.serializers import TimeTableUserSerializer, TimeTableSerializer, ScoreStudentSerializer
from school_structure.models import TimeTable, EducationalСlass
from users.models import StaffUser, Student, User
from .permissions import EducationClassesPermissions, MixedPermission
from .serializers import StaffUserSerializer, StudentSerializer


class StudentsResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StaffListView(viewsets.ModelViewSet):

    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer

class StudentsListView(MixedPermission, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentsResultsSetPagination
    permission_classes_by_action = {
        'student_timetable': [EducationClassesPermissions,],
        'students_scores': [EducationClassesPermissions,]
    }

    @action(methods=['GET'], detail=True)
    def student_timetable(self, *args, **kwargs):
        print(self.action)
        student = self.get_object()
        timetable = TimeTable.objects.filter(classes__id=student.educational_class_id)
        if timetable:
            serializer = TimeTableUserSerializer(timetable, many=True, context={'request': self.request})
            return Response(serializer.data)
        return Response(timetable)

    @action(methods=['GET'], detail=True)
    def students_scores(self, *args, **kwargs):
        student = self.get_object()
        # @ TODO Нужна ли проверка
        serializer = ScoreStudentSerializer(student.score.all().order_by('subject'), many=True)
        return Response(serializer.data)


















