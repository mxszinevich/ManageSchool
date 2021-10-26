from django.urls import path
from users.api.views import (
    StaffListView,
    StudentsListView,
    ParentsStudentView,
)

urlpatterns = [
    path('staff', StaffListView.as_view({'get': 'list', 'post': 'create'}), name='staff'),
    path('staff/<int:pk>/', StaffListView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('students', StudentsListView.as_view({'get': 'list', 'post': 'create'})),
    path('parents', ParentsStudentView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('parents/<int:pk>', ParentsStudentView.as_view({'put': 'update'})),
    path('students/<int:pk>', StudentsListView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('students/<int:pk>/timetable/', StudentsListView.as_view({'get': 'student_timetable'})),
    path('students/<int:pk>/scores/', StudentsListView.as_view({'get': 'students_scores'})),
]
