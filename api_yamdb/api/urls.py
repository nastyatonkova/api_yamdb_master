from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'
router = routers.SimpleRouter()


router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
