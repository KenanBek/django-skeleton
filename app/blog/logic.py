from django.db.models import Q
from django.shortcuts import get_object_or_404

from core import abstracts
from . import models


class BlogLogic(abstracts.LogicAbstract):
    def __init__(self, request):
        super(BlogLogic, self).__init__(request)

    def page(self, page_slug):
        return get_object_or_404(models.Page, slug=page_slug, status=models.ITEM_STATUS_PUBLISHED)

    def pages(self, page_number=None):
        return models.Page.objects.filter(status=models.ITEM_STATUS_PUBLISHED).all()

    def post(self, post_id, post_slug):
        return get_object_or_404(models.Post, pk=post_id, slug=post_slug, status=models.ITEM_STATUS_PUBLISHED)

    def posts(self, page_number=None):
        return models.Post.objects.filter(status=models.ITEM_STATUS_PUBLISHED).order_by('-modified_at').all()

    def search(self, term):
        pages = models.Page.objects.filter(Q(title__contains=term) | Q(content__contains=term))
        posts = models.Post.objects.filter((Q(title__contains=term)
                                            | Q(short_content__contains=term)
                                            | Q(full_content__contains=term))
                                           & Q(status=models.ITEM_STATUS_PUBLISHED))
        return {
            "pages": pages,
            "posts": posts
        }

    def new_subscription(self, name, email):
        subscriber = models.Subscriber()
        subscriber.name = name
        subscriber.email = email
        subscriber.save()

