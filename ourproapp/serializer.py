# -*- coding:UTF-8 -*-

from rest_framework import serializers
from models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "user_name", "user_password")