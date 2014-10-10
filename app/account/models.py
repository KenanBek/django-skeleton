from django.db import models

from core import models as core_models


class User(core_models.Model):
    email = models.EmailField()
    pass

