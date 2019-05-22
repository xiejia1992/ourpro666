# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    '''  定义用户模型 '''
    user_name = models.CharField(max_length=128)
    user_password = models.CharField(max_length=64)

    def __unicode__(self):
        return self.user_name