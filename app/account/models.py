from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save

from core import models as core_models


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Profile(core_models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to='account/avatar', null=True, blank=True)

    def __str__(self):
        return self.user.username

