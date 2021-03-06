from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.api.views import (
    TokenObtainView,
    StaffUserRegisterView,
    StudentUserRegisterView
)

schema_view = get_schema_view(
    openapi.Info(
        title=" ManageSchool API",
        default_version='v1',
    ),
    public=True)

urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/school/', include('school_structure.urls')),
    path('auth/', include('djoser.urls')),  # URLS
    path('auth/login/', TokenObtainView.as_view(), name='token_create'),
    path('auth/registration/staffuser', StaffUserRegisterView.as_view({'post': 'create'}), name='staff_create'),
    path('auth/registration/students', StudentUserRegisterView.as_view({'post': 'create'}), name='students_create'),
    path('auth/', include('djoser.urls.jwt')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
