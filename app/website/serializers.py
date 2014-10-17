from rest_framework.serializers import ModelSerializer
import models


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id', 'title', 'short_content',)

