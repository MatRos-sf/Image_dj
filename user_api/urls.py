from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet

router = DefaultRouter()

router.register(
    r'profile',
    ProfileViewSet,
    basename="profile"
)

urlpatterns = [
    re_path(r'', include(router.urls))
]