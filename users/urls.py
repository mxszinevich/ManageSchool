from django.urls import path
from users.api.views import (
    StaffListView,
    StudentsListView,
)

urlpatterns = [
    path('staff', StaffListView.as_view({'get':'list', 'post':'create'})),
    path('students', StudentsListView.as_view({'get':'list', 'post':'create'})),
    path('students/<int:pk>', StudentsListView.as_view({'get':'retrieve', 'put':'update'})),
    path('students/<int:pk>/timetable/', StudentsListView.as_view({'get':'student_timetable'})),
    path('students/<int:pk>/scores/', StudentsListView.as_view({'get':'students_scores'})),
]