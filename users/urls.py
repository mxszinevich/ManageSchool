from django.urls import path
from users.api.views import StaffListView

urlpatterns = [
    path('users_list', StaffListView.as_view({'get':'list','post':'create'})),
]