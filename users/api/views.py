from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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

    # def update(self, request, *args, **kwargs):
    #     update_student = get_object_or_404(Student.objects.all(), pk=kwargs['pk'])
    #     serializer = StudentSerializer(instance=update_student, data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         update_student = serializer.save()
    #     return  Response({'success':f'{update_student} updated'})







