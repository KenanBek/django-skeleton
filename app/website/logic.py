from django.db.models import Q

from website.models import PUBLISHED

from website.models import Page, Post


def get_page(page_slug):
    return Page.objects.get(slug=page_slug, status=PUBLISHED)


def load_pages():
    return Page.objects.filter(status=PUBLISHED).all()


def get_post(post_id, post_slug):
    return Post.objects.get(pk=post_id, slug=post_slug, status=PUBLISHED)


def load_posts():
    return Post.objects.filter(status=PUBLISHED).all()


class SearchResult:
    pages = ""
    posts = ""

    def __init__(self, pages, posts):
        self.pages = pages
        self.posts = posts


def search(term):
    pages = Page.objects.filter(Q(title__contains=term) | Q(content__contains=term))
    posts = Post.objects.filter((Q(title__contains=term)
                                 | Q(short_content__contains=term)
                                 | Q(full_content__contains=term))
                                & Q(status=PUBLISHED))
    return SearchResult(pages, posts)

