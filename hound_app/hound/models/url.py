from django.db import models
from django.forms import ModelForm
import datetime

class Url(models.Model):
    url = models.CharField("Url", blank=False, max_length=32, unique=True)
    expires = models.DateTimeField("Expires")

    @classmethod
    def create(cls, hash):
        url = cls(url=hash,expires = datetime.datetime.now()+datetime.timedelta(minutes = 15))
        return url

