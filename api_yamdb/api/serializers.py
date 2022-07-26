from rest_framework import serializers
from reviews.models import Reviews, Comments


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
