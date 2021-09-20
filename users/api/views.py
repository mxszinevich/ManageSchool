from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from users.models import StaffUser, Student
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

