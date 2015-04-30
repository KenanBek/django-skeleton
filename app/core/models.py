from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import abstracts

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


class Settings(abstracts.ModelAbstract):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=1024)
    group = models.CharField(max_length=256, null=True, blank=True, default='')

    def __str__(self):
        return u"Settings: {} ({}) = {}".format(self.key, self.group, self.value)

    def __unicode__(self):
        return self.__str__()

    def clean_fields(self, exclude=None):
        errors = {}
        if self.key == 'groups':
            errors['key'] = _("'groups' word is reserved.")
        if self.group == 'groups':
            errors['group'] = _("'groups' word is reserved.")
        if errors:
            raise ValidationError(errors)
        super(Settings, self).clean_fields(exclude)

    class Meta:
        unique_together = ('group', 'key', )


class Event(abstracts.ModelAbstract):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return u"{} ({})".format(self.title, self.added_at.date())

    def __unicode__(self):
        return self.__str__()


class Log(abstracts.ModelAbstract):
    event = models.ForeignKey(Event)
    level = models.IntegerField(choices=LOG_LEVEL_CHOICES, default=LOG_LEVEL_DEBUG)
    text = models.CharField(max_length=1024)

    def __str__(self):
        return u"{} {} {}".format(self.event, self.added_at.time(), self.text)

    def __unicode__(self):
        return self.__str__()


class Request(abstracts.ModelAbstract):
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

