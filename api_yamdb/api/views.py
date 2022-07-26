from rest_framework import viewsets
from reviews.models import Reviews, Comments, Titles
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = Reviews.objects.filter(title=title_id)
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        reviews = Reviews.objects.filter(title=title_id)
        comments = reviews.comments.filter(review=review_id)
        return comments

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )
