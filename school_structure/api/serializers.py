from rest_framework import serializers

from school_structure.models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields = ('__all__')