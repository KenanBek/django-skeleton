from django.db import models
from django.contrib.auth.models import User
import datetime
from core import abstracts
from core.utils import helpers


''' Types '''

REQUEST_TYPE_ACCOUNT = 1
REQUEST_TYPE_EMAIL = 2
REQUEST_TYPE_PASSWORD = 3
REQUEST_TYPE_CHOICES = (
    (REQUEST_TYPE_ACCOUNT, "Account Verify"),
    (REQUEST_TYPE_EMAIL, "Email Change"),
    (REQUEST_TYPE_PASSWORD, "Password Reset"),
)


def get_account_file_name(instance, filename):
    return helpers.get_file_filename(instance, filename, "account")


class Profile(abstracts.ModelAbstract):
    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True)
    avatar = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_account_file_name)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return u"{}".format(self.user.username)

    def __unicode__(self):
        return self.__str__()


class Request(abstracts.ModelAbstract):
    user = models.ForeignKey(User)
    type = models.SmallIntegerField(choices=REQUEST_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=64, blank=True)
    key_expires_at = models.DateTimeField(auto_now_add=True)
    str_field_1 = models.CharField(max_length=64, null=True, blank=True)
    str_field_2 = models.CharField(max_length=64, null=True, blank=True)
    dec_field_1 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    dec_field_2 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    bool_field_1 = models.BooleanField(default=False, blank=True)
    bool_field_2 = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return u"{}".format(self.user.username)

    def __unicode__(self):
        return self.__str__()


