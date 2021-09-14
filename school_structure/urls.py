from django.urls import path
from .api.views import SchoolView,EducationalСlassSerializer

urlpatterns = [
    path('info', SchoolView.as_view({'get':'list','post':'create'})),
    path('classes', EducationalСlassSerializer.as_view({'get':'list','post':'create'})),
]