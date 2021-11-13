from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from datetime import date

from school_structure.api.serializers import TimeTableUserSerializer, ScoreStudentSerializer
from school_structure.models import TimeTable
from users.models import StaffUser, Student, User, ParentsStudent
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
    UpdateStudentSerializer, RegistrationStaffUserSerializer, RegistrationStudentUserSerializer,
    ParentsStudentSerializer
)
from ..tasks import generate_students_reports
from ..serializers import CustomTokenObtainSerializer
from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings as djoser_settings

class TokenObtainView(TokenViewBase):
    """Кастомное представление получения jwt-токена"""
    serializer_class = CustomTokenObtainSerializer


class StudentsResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StaffListView(MixedPermission, viewsets.ModelViewSet):
    """Представление для сотрудников"""
    queryset = StaffUser.objects.select_related('user').all()
    serializer_class = ReadAllStaffUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    staff_serializer_class_by_action = {
        'update': UpdateStaffUserSerializer,
        'list': StaffUserSerializer,
        'create': StaffUserSerializer,
    }

    permission_classes_by_action = {
        'update': [StaffUserPermissions],
        'create': [StaffUserPermissions],  # Создать сотрудника может только персонал
        'destroy': [StaffUserPermissions]
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
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    permission_classes = [StudentUserPermissions]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_fields = ['user__email', 'user__last_name']  # @TODO Фильтр по user__last_name не работает
    # search_fields = ['id'] # TODO почему не работает?
    permission_classes_by_action = {
        'student_timetable': [StudentInfoPermissions, ],
        'students_scores': [StudentInfoPermissions, ],
        'update': [StaffUserPermissions, ],
        'retrieve': [StudentInfoPermissions, ],
        'receive_reports': [StudentUserPermissions, ],
    }
    serializer_class_by_action = {
        'update': UpdateStudentSerializer
    }

    @method_decorator(cache_page(60*60))  # кеширование данных на 1 час
    def list(self, request, *args, **kwargs):
        return super(StudentsListView, self).list(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def student_timetable(self, *args, **kwargs):
        """Метод получение расписания студента"""
        student = self.get_object()
        timetable = TimeTable.objects.filter(classes__id=student.educational_class_id)
        if timetable:
            serializer = TimeTableUserSerializer(timetable, many=True, context={'request': self.request})
            return Response(serializer.data)
        return Response(timetable)

    @action(methods=['GET'], detail=True)
    def students_scores(self, *args, **kwargs):
        """Метод получение оценок студентов"""
        student = self.get_object()
        # Фильтрация оценок по предмету
        query_params = args[0].query_params  # Request
        subject_filter = Q()
        value_filter = Q()
        month_filter = Q()
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

    @action(methods=['GET'], detail=False)
    def receive_reports(self, *args, **kwargs):
        """Метод генерирования отчета"""
        generate_students_reports.delay()
        return Response('Отчет формируется')


class ParentsStudentView(viewsets.ModelViewSet):
    """Представление родителей студента"""
    queryset = ParentsStudent.objects.all()
    serializer_class = ParentsStudentSerializer
    permission_classes = [StudentUserPermissions]


class BaseUserRegistrationView(UserViewSet):
    """
    https://github.com/sunscrapers/djoser/blob/master/djoser/views.py
    Представление для регистрации пользователей школы с подтверждением email(djoser)
    """
    # @ TODO зачем perform_create
    def perform_create(self, serializer):
        user_registration = serializer.save()
        user = user_registration.user
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            djoser_settings.EMAIL.activation(self.request, context).send(to)
        elif djoser_settings.SEND_CONFIRMATION_EMAIL:
            djoser_settings.EMAIL.confirmation(self.request, context).send(to)

    def get_serializer_class(self):
        if self.action == 'create':
            if djoser_settings.USER_CREATE_PASSWORD_RETYPE:
                return djoser_settings.SERIALIZERS.user_create_password_retype
            return self.serializer_class
        return None


class StaffUserRegisterView(BaseUserRegistrationView):
    """Представление для регистрации сотрудников школы с подтверждением email(djoser)"""
    serializer_class = RegistrationStaffUserSerializer


class StudentUserRegisterView(BaseUserRegistrationView):
    """Представление для регистрации студентов школы с подтверждением email(djoser)"""
    serializer_class = RegistrationStudentUserSerializer

