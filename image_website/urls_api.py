from django.urls import path, include

urlpatterns = [
    path('p/', include('user_api.urls')),
    path('i/', include('image_api.urls')),
]