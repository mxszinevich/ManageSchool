from django.urls import path
from .api.views import (
    SchoolView,
    EducationalСlassView,
    SubjectView,
    TimeTableView
)

urlpatterns = [
    path('info', SchoolView.as_view({'get': 'list', 'post': 'create'})),
    path('classes', EducationalСlassView.as_view({'get': 'list', 'post': 'create'})),
    path('classes/<int:pk>', EducationalСlassView.as_view({'get': 'retrieve'})),
    path('classes/<int:pk>/timetable', EducationalСlassView.as_view({'get': 'education_class_timetable'})),
    path('subjects', SubjectView.as_view({'get': 'list', 'post': 'create'})),
    path('subjects/<int:pk>', SubjectView.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy'})),
    path('timetable', TimeTableView.as_view({'get': 'list', 'post': 'create'})),
    path('timetable/<int:pk>', TimeTableView.as_view({'get': 'retrieve'})),
]
