from django.urls import path, include

from .views import create_default_profile_tier
urlpatterns = [

    path("first_run/", create_default_profile_tier, name='set_website'),
]