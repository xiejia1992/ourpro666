# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    '''  定义用户模型 '''
    user_id = models.CharField(max_length=14, primary_key=True)
    user_image = models.CharField(max_length=64)
    user_mobile = models.CharField(max_length=11)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=256)

    def __unicode__(self):
        return self.user_mobile + self.user_email
