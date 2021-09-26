from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from school_structure.models import *
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
    queryset = School.objects.all_with_counts()
    serializer_class = SchoolSerializer

class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class EducationalСlassView(viewsets.ModelViewSet):
    queryset = EducationalСlass.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListEducationalСlassSerializer
        return EducationalСlassSerializer


class TimeTableView(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer






