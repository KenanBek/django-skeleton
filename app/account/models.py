from django.db import models
from django.contrib.auth.models import User

from core import models as core_models


class Profile(core_models.ModelAbstract):
    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to='account/avatar', null=True, blank=True)

    def __str__(self):
        return self.user.username

