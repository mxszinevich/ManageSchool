from rest_framework import viewsets
from school_structure.models import *
from .serializers import SchoolSerializer,EducationalСlassSerializer

class SchoolView(viewsets.ModelViewSet):
    queryset=School.objects.all()
    serializer_class=SchoolSerializer

class EducationalСlassSerializer(viewsets.ModelViewSet):
    queryset=EducationalСlass.objects.all()
    serializer_class=EducationalСlassSerializer