from django.urls import path, include

from .views import create_default_profile_tier_view
urlpatterns = [

    path("first_run/", create_default_profile_tier_view, name='set_website'),
]