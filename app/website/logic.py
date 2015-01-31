from django.db.models import Q
from django.shortcuts import get_object_or_404

import models


def get_page(page_slug):
    return get_object_or_404(models.Page, slug=page_slug, status=models.ITEM_STATUS_PUBLISHED)


def load_pages():
    return models.Page.objects.filter(status=models.ITEM_STATUS_PUBLISHED).all()


def get_post(post_id, post_slug):
    return get_object_or_404(models.Post, pk=post_id, slug=post_slug, status=models.ITEM_STATUS_PUBLISHED)


def load_posts():
    return models.Post.objects.filter(status=models.ITEM_STATUS_PUBLISHED).order_by('-modified_at').all()


class SearchResult:
    pages = ""
    posts = ""

    def __init__(self, pages, posts):
        self.pages = pages
        self.posts = posts


def search(term):
    pages = models.Page.objects.filter(Q(title__contains=term) | Q(content__contains=term))
    posts = models.Post.objects.filter((Q(title__contains=term)
                                        | Q(short_content__contains=term)
                                        | Q(full_content__contains=term))
                                       & Q(status=models.ITEM_STATUS_PUBLISHED))
    return SearchResult(pages, posts)


def subscribe(name, email):
    subscriber = models.Subscriber()
    subscriber.name = name
    subscriber.email = email
    subscriber.save()

