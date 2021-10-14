from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from datetime import date

from school_structure.api.serializers import TimeTableUserSerializer, ScoreStudentSerializer
from school_structure.models import TimeTable
from users.models import StaffUser, Student, User
from .mixins import MixedPermission, MixedPermissionSerializer
from .permissions import (
    StaffUserPermissions,
    StudentUserPermissions,
    StudentInfoPermissions
)
from .serializers import (
    StaffUserSerializer,
    StudentSerializer,
    UpdateStaffUserSerializer,
    ReadAllStaffUserSerializer,
    UpdateStudentSerializer
)
from ..serializers import CustomTokenObtainSerializer


class TokenObtainView(TokenViewBase):
    """Кастомное представление получения jwt-токена"""
    serializer_class = CustomTokenObtainSerializer


class StudentsResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StaffListView(MixedPermission, viewsets.ModelViewSet):
    """Представление для сотрудников"""
    queryset = StaffUser.objects.all()
    serializer_class = ReadAllStaffUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    staff_serializer_class_by_action = {
        'update': UpdateStaffUserSerializer,
        'list': StaffUserSerializer,
        'create': StaffUserSerializer,
    }

    permission_classes_by_action = {
        'update': [StaffUserPermissions, ],
        'create': [StaffUserPermissions, ],
        'destroy': [StaffUserPermissions, ]
    }

    def get_serializer_class(self):
        try:
            user = self.request.user
            if user.is_staff or getattr(user, 'staff'):  # Доступ к полной информации получает только staff и superuser
                serializer_class = self.staff_serializer_class_by_action[self.action]
        except (KeyError, AttributeError):
            serializer_class = self.serializer_class
        return serializer_class


class StudentsListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Представления для студентов"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentsResultsSetPagination
    permission_classes = [StudentUserPermissions]
    permission_classes_by_action = {
        'student_timetable': [StudentInfoPermissions, ],
        'students_scores': [StudentInfoPermissions, ],
        'update': [StudentInfoPermissions, ],
        'retrieve': [StudentInfoPermissions, ],
    }
    serializer_class_by_action = {
        'update': UpdateStudentSerializer
    }

    @action(methods=['GET'], detail=True)
    def student_timetable(self, *args, **kwargs):
        """Метод получение расписания конкретного студента"""
        student = self.get_object()
        timetable = TimeTable.objects.filter(classes__id=student.educational_class_id)
        if timetable:
            serializer = TimeTableUserSerializer(timetable, many=True, context={'request': self.request})
            return Response(serializer.data)
        return Response(timetable)

    # @TODO django-filter
    # @TODO параметры get запроса в документацию

    @action(methods=['GET'], detail=True)
    def students_scores(self, *args, **kwargs):
        """Метод получение оценок студентов"""
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
                    subject_filter = Q(subject_id__in=query_params.getlist('subject'))
                if query_params.getlist('value'):
                    value_filter = Q(value__in=query_params.getlist('value'))
                if query_params.getlist('month'):
                    month_filter = Q(
                        date__month__in=query_params.getlist('month'),
                        date__year=date.today().year
                    )
            except ValueError:
                raise APIException('Неверный параметр запроса')

        scores_filter = subject_filter & value_filter & month_filter
        serializer = ScoreStudentSerializer(student.score.filter(scores_filter).order_by('subject'), many=True)

        return Response(serializer.data)
