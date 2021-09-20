from django.urls import path
from .api.views import SchoolView,EducationalСlassView

urlpatterns = [
    path('info', SchoolView.as_view({'get':'list','post':'create'})),
    path('classes', EducationalСlassView.as_view({'get':'list','post':'create'})),
    path('classes/<int:pk>', EducationalСlassView.as_view({'get':'retrieve'})),
]