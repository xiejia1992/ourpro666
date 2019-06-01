# -*- coding:UTF-8 -*-
from rest_framework import serializers
from models import User


class ResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(label='status_code', read_only=True)
    message = serializers.CharField(label='message', max_length=1024)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "user_mobile", "user_email")