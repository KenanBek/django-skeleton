from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from core import abstracts
from core.utils import helpers


def get_blog_file_name(instance, filename):
    return helpers.get_file_filename(instance, filename, "blog")


def get_blog_document_file_name(instance, filename):
    return helpers.get_file_filename(instance, filename, "blog/documents")


''' Types '''

ITEM_STATUS_PUBLISHED = 1
ITEM_STATUS_HIDDEN = 2
ITEM_STATUS_CHOICES = (
    (ITEM_STATUS_PUBLISHED, "Published"),
    (ITEM_STATUS_HIDDEN, "Hidden"),
)

''' Slider '''


class Slider(abstracts.ModelAbstract):
    status = models.IntegerField(max_length=9, choices=ITEM_STATUS_CHOICES, default=ITEM_STATUS_PUBLISHED)
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()


class Slide(abstracts.ModelAbstract):
    status = models.IntegerField(max_length=9, choices=ITEM_STATUS_CHOICES, default=ITEM_STATUS_PUBLISHED)
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_blog_file_name)
    related_slider = models.ForeignKey(Slider)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()


''' Page '''


class Widget(abstracts.ModelAbstract):
    title = models.CharField(max_length=32)
    content = models.TextField()
    featured_image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_blog_file_name)
    link_title = models.CharField(max_length=32, null=True, blank=True)
    link_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()


class Page(abstracts.ModelAbstract):
    status = models.IntegerField(max_length=9, choices=ITEM_STATUS_CHOICES, default=ITEM_STATUS_PUBLISHED)
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True, editable=False)
    content = models.TextField()
    widgets = models.ManyToManyField(Widget, null=True, blank=True)
    featured_image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_blog_file_name)
    related_slider = models.ForeignKey(Slider, null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def get_widgets(self):
        return self.widgets.all()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Page, self).save(*args, **kwargs)


''' Post '''


class Category(abstracts.ModelAbstract):
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True, editable=False)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Category, self).save(*args, **kwargs)


class Post(abstracts.ModelAbstract):
    status = models.IntegerField(max_length=9, choices=ITEM_STATUS_CHOICES, default=ITEM_STATUS_PUBLISHED)
    title = models.CharField(max_length=32)
    slug = models.SlugField(editable=False)
    short_content = models.CharField(max_length=512)
    full_content = models.TextField()
    categories = models.ManyToManyField(Category)
    featured_image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_blog_file_name)
    related_slider = models.ForeignKey(Slider, null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={'post_id': self.pk, 'post_slug': self.slug})


''' Beep '''


class Beep(abstracts.ModelAbstract):
    text = models.TextField(max_length=128)
    user = models.ForeignKey(User, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True, editable=False, )

    def __str__(self):
        return u"{}".format(self.text)

    def __unicode__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('blog_beep_edit', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
            update_fields=None):
        if (update_fields and 'text' in update_fields) or (not update_fields):
            self.length = len(self.text)
        super(Beep, self).save(force_insert, force_update, using, update_fields)


''' Subscriber & Document '''


class Subscriber(abstracts.ModelAbstract):
    name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)

    def __str__(self):
        return u"{} ({})".format(self.name, self.email)

    def __unicode__(self):
        return self.__str__()


class Document(abstracts.ModelAbstract):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    short_description = models.CharField(max_length=128)
    document_file = models.FileField(upload_to=get_blog_document_file_name)

    def __str__(self):
        return u"'{0}' attached document with '{1}' description".format(self.name, self.short_description)

    def __unicode__(self):
        return self.__str__()


''' Contact '''


class Contact(abstracts.ModelAbstract):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    subject = models.CharField(max_length=32)
    message = models.TextField()

    def __str__(self):
        return u"'{0}' submit contact with '{1}' subject".format(self.name, self.subject)

    def __unicode__(self):
        return self.__str__()

