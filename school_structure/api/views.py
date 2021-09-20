from rest_framework import viewsets
from rest_framework.response import Response

from school_structure.models import *
from .serializers import SchoolSerializer,EducationalСlassSerializer

class SchoolView(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class EducationalСlassView(viewsets.ModelViewSet):
    queryset = EducationalСlass.objects.all()
    serializer_class = EducationalСlassSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if name:
            request.data['name'] = name.replace(' ', '')
        return  super().create(request, *args, **kwargs)






