from django.db import models
from django.contrib.auth.models import User

from core import abstracts
from core.utils import helpers


def get_account_file_name(instance, filename):
    return helpers.get_file_filename(instance, filename, "account")


class Profile(abstracts.ModelAbstract):
    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True)
    avatar = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_account_file_name)

    def __str__(self):
        return u"{}{}".format(self.user.username)

    def __unicode__(self):
        return self.__str__()

