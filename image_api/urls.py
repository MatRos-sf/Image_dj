from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter


from .views import ImageViewSet, GalleryViewSet

router = DefaultRouter()

router.register(
    r'images',
    ImageViewSet,
    basename="images"
)
router.register(
    r'gallery',
    GalleryViewSet,
    basename="gallery"
)

urlpatterns = [
    re_path(r'', include(router.urls)),
]