from rest_framework import viewsets, permissions

from . import models
from . import serializers


class PageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    permission_classes = (permissions.IsAdminUser, )

    def pre_save(self, obj):
        obj.owner = self.request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAdminUser, )

    def pre_save(self, obj):
        obj.owner = self.request.user

