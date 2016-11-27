from __future__ import unicode_literals

from django.db import models
from accounts.models import MyUser

class R(models.Model):
    user = models.ForeignKey(MyUser)
    title = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField()
    apply_ = models.TextField()
    timestamp = models.DateTimeFIeld(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.title
