from rest_framework import viewsets
from rest_framework.response import Response

from users.models import StaffUser
from .serializers import  StaffUserSerializer

class StaffListView(viewsets.ModelViewSet):

    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer


