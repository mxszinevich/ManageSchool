from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from datetime import date

from rest_framework_simplejwt.views import TokenViewBase

from school_structure.api.serializers import TimeTableUserSerializer, ScoreStudentSerializer
from school_structure.models import TimeTable
from users.models import StaffUser, Student
from .permissions import EducationClassesPermissions, MixedPermission
from .serializers import StaffUserSerializer, StudentSerializer
from ..serializers import CustomTokenObtainSerializer


class TokenObtainView(TokenViewBase):
    serializer_class = CustomTokenObtainSerializer


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
    permission_classes = [EducationClassesPermissions]
    permission_classes_by_action = {
        'student_timetable': [EducationClassesPermissions, ],
        'students_scores': [EducationClassesPermissions, ]
    }

    @action(methods=['GET'], detail=True)
    def student_timetable(self, *args, **kwargs):
        student = self.get_object()
        # self.check_object_permissions(self.request, obj)
        timetable = TimeTable.objects.filter(classes__id=student.educational_class_id)
        if timetable:
            serializer = TimeTableUserSerializer(timetable, many=True, context={'request': self.request})
            return Response(serializer.data)
        return Response(timetable)

    # @TODO django-filter
    # @TODO параметры get запроса в документацию
    # @TODO get_queryset
    @action(methods=['GET'], detail=True)
    def students_scores(self, *args, **kwargs):
        student = self.get_object()
        # Фильтрация оценок по предмету

        query_params = args[0].query_params  # Request
        subject_filter = Q()
        value_filter = Q()
        month_filter = Q()
        print(query_params.getlist('subject'))
        if query_params:
            try:
                if query_params.getlist('subject'):
                    subject_filter = Q(subject_id__in=list(map(int, query_params.getlist('subject'))))
                if query_params.getlist('value'):
                    value_filter = Q(value__in=list(map(int, query_params.getlist('value'))))
                if query_params.getlist('month'):
                    month_filter = Q(
                        date__month__in=list(map(int, query_params.getlist('month'))),
                        date__year=date.today().year
                    )
            except ValueError:
                raise APIException('Неверный параметр запроса')

        scores_filter = subject_filter & value_filter & month_filter
        serializer = ScoreStudentSerializer(student.score.filter(scores_filter).order_by('subject'), many=True)

        return Response(serializer.data)
