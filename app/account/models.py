from django.db import models
from django.contrib.auth.models import User

from core import utils
from core import models as core_models


def get_account_file_name(instance, filename):
    return utils.get_file_filename(instance, filename, "account")


class Profile(core_models.ModelAbstract):
    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True)
    avatar = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_account_file_name)

    def __str__(self):
        return self.user.username

