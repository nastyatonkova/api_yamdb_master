from django.db.models import Avg
from reviews.models import Category, Genre, Title
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import ModelMixinSet
from rest_framework.viewsets import ModelViewSet
from api.filters import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from .permissions import (IsAdminUserOrReadOnly)


class CategoryViewSet(ModelMixinSet):
    """
    Receive all categoriers. Available without token.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """
    Receive all genries. Available without token.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """
    Receive all titles. Available without token.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
