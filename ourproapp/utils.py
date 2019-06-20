# -*- coding: utf-8 -*-

import time
import hashlib
import base64
import random
from django.core import signing
from django.core.cache import cache
from rest_framework.response import Response
from serializer import ResponseSerializer
from models import User

#defalut config about token
HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'our_pro_666'
SALT = 'www.ourpro.cn'
TIME_OUT = 10 * 60


def create_user_id():
    timestamp = str(int(time.time()))
    random_int = str(random.randint(0000, 9999))
    user_id = random_int[:2] + timestamp[:5] + random_int[2:] + timestamp[5:]
    return user_id


def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(user_id):
    """生成token信息"""
    header = encrypt(HEADER)
    payload = {"user_id": user_id, "iat": time.time()}
    payload = encrypt(payload)
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    cache.set(user_id + '_Token', token, TIME_OUT)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


def get_user_id(token):
    payload = get_payload(token)
    return payload['user_id']


def check_token(func):
    def wrapper(request, *args, **kwargs):
        _response = {'message': "Token has expired", 'status_code': 403}
        if request.META['HTTP_AUTH']:
            _token = request.META['HTTP_AUTH']
            user_id = get_user_id(_token)
            last_token = cache.get(user_id + '_Token')
            if last_token:
                if last_token == _token:
                    cache.set(user_id + '_Token', _token, TIME_OUT)
                    return func(request, user_id, *args, **kwargs)
                return Response(ResponseSerializer(_response).data)
            return Response(ResponseSerializer(_response).data)
        return Response(ResponseSerializer(_response).data)
    return wrapper


def check_user_login(user, password):
    try:
        if '@' in user:
            user = User.objects.get(user_email=user)
        else:
            user = User.objects.get(user_mobile=user)
    except User.DoesNotExist:
        return None
    if user:
        if user.user_password == base64.encodestring(password):
            return user.user_id
    return False


def check_user_exists(user):
    if User.objects.filter(user_mobile=user) or User.objects.filter(user_email=user):
        return True


def check_register_code(user, identifying_code):
    if cache.get(user + "_identifying_code") == identifying_code:
        return True
