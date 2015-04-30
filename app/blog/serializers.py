from rest_framework.serializers import ModelSerializer

from . import models


class PageSerializer(ModelSerializer):
    class Meta:
        model = models.Page
        fields = ('id', 'title', 'featured_image', 'content', )


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id', 'title', 'featured_image', 'short_content', 'full_content', )

