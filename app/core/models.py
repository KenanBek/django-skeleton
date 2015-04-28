"""
Base model classes. Used in other applications.
"""
from django.db import models
from django.contrib import admin

''' Abstract classes '''


class ModelAbstract(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class ModelAdminAbstract(admin.ModelAdmin):
    pass


''' Core entities '''

LOG_LEVEL_DEBUG = 1
LOG_LEVEL_INFO = 2
LOG_LEVEL_WARNING = 3
LOG_LEVEL_ERROR = 4
LOG_LEVEL_CRITICAL = 5
LOG_LEVEL_CHOICES = (
    (LOG_LEVEL_DEBUG, 'Debug'),
    (LOG_LEVEL_INFO, 'Info'),
    (LOG_LEVEL_WARNING, 'Warning'),
    (LOG_LEVEL_ERROR, 'Error'),
    (LOG_LEVEL_CRITICAL, 'Critical'),
)


class Event(ModelAbstract):
    uuid = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256, default=u"<not defined>")

    def __str__(self):
        return u"{} ({})".format(self.identifier, self.added_at.date())

    def __unicode__(self):
        return self.__str__()


class Log(ModelAbstract):
    event = models.ForeignKey(Event)
    level = models.IntegerField(choices=LOG_LEVEL_CHOICES, default=LOG_LEVEL_DEBUG)
    text = models.CharField(max_length=1024)

    def __str__(self):
        return u"{} {} {}".format(self.event, self.added_at.time(), self.text)

    def __unicode__(self):
        return self.__str__()


class Request(ModelAbstract):
    user_username = models.CharField(max_length=30, null=True, blank=True)
    user_is_staff = models.BooleanField(default=False)
    user_is_active = models.BooleanField(default=False)

    client_name = models.CharField(max_length=512, null=True, blank=True)
    client_ip = models.IPAddressField(null=True, blank=True)
    client_real_ip = models.IPAddressField(null=True, blank=True)
    client_agent = models.CharField(max_length=512, null=True, blank=True)

    server_name = models.CharField(max_length=512, null=True, blank=True)
    server_host = models.CharField(max_length=512, null=True, blank=True)

    scheme = models.CharField(max_length=16, null=True, blank=True)
    method = models.CharField(max_length=16, null=True, blank=True)
    data = models.TextField(null=True, blank=True)

    is_ajax = models.BooleanField(default=False)

    from_page = models.CharField(max_length=1024, null=True, blank=True)
    to_page = models.CharField(max_length=1024, null=True, blank=True)
    to_page_query = models.CharField(max_length=1024, null=True, blank=True)

