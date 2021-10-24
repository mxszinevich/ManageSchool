from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from school_structure.models import *
from .mixins import MixinSerializer, MixinPermissions, MixedPermissionSerializer
from .permissions import SchoolBaseAdministrationPermissions, SchoolStaffPermissions
from .serializers import (
    SchoolSerializer,
    EducationalСlassSerializer,
    ListEducationalСlassSerializer,
    SubjectSerializer,
    TimeTableSerializer, TimeTableBaseSerializer
)


class SchoolPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SchoolView(viewsets.ModelViewSet):
    """Представление школы"""
    queryset = School.objects.all_with_counts()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubjectView(MixinPermissions, viewsets.ModelViewSet):
    """Представление школьного предмета"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [SchoolBaseAdministrationPermissions]
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly]
    }


class EducationalСlassView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Представление класса"""
    queryset = EducationalСlass.objects.all()
    serializer_class = EducationalСlassSerializer
    permission_classes = [SchoolBaseAdministrationPermissions]
    serializer_class_by_action = {
        'list': ListEducationalСlassSerializer
    }
    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'education_class_timetable': [IsAuthenticated],
        'retrieve': [SchoolStaffPermissions]
    }

    @action(methods=['GET'], detail=True)
    def education_class_timetable(self, *args, **kwargs):
        """Метод получение расписания класса"""
        education_class = self.get_object()
        timetable = education_class.timetable.all()
        serializer = TimeTableBaseSerializer(timetable, many=True)
        return Response(serializer.data)


class TimeTableView(MixinPermissions, viewsets.ModelViewSet):
    """Представление расписания"""
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [SchoolBaseAdministrationPermissions]
    permission_classes_by_action = {
        'list': [IsAuthenticated]
    }
