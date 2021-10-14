from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from school_structure.models import *
from .mixins import MixinSerializer
from .serializers import (
    SchoolSerializer,
    EducationalСlassSerializer,
    ListEducationalСlassSerializer,
    SubjectSerializer,
    TimeTableSerializer
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


class SubjectView(viewsets.ModelViewSet):
    """Представление предмета"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer



class EducationalСlassView(MixinSerializer, viewsets.ModelViewSet):
    """Представление класса"""
    queryset = EducationalСlass.objects.all()
    serializer_class = EducationalСlassSerializer
    serializer_class_by_action = {
        'list': ListEducationalСlassSerializer
    }

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return ListEducationalСlassSerializer
    #     return EducationalСlassSerializer


class TimeTableView(viewsets.ModelViewSet):
    """Представление расписания"""
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
