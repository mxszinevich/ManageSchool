from django.urls import path
from .api.views import SchoolView

urlpatterns = [
    path('info', SchoolView.as_view({'get':'list','post':'create'})),
]