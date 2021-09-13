from rest_framework import viewsets
from school_structure.models import *
from .serializers import SchoolSerializer

class SchoolView(viewsets.ModelViewSet):
    queryset=School.objects.all()
    serializer_class=SchoolSerializer
