from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter


from .views import ImageViewSet, GalleryViewSet, ImagesUserViewSet

router = DefaultRouter()

router.register(
    r'images',
    ImageViewSet,
    basename="api_images"
)
router.register(
    r'gallery',
    GalleryViewSet,
    basename="api_gallery"
)
router.register(
    r'ownimages',
    ImagesUserViewSet,
    basename="api_ownimages"
)

urlpatterns = [
    re_path(r'', include(router.urls)),
]