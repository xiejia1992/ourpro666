# -*- coding: utf-8 -*-

import time
import hashlib
import base64
from django.core import signing
from django.core.cache import cache
from models import User

#defalut config about token
HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'our_pro_666'
SALT = 'www.ourpro.cn'
TIME_OUT = 5 * 60


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


def create_token(username):
    """生成token信息"""
    header = encrypt(HEADER)
    payload = {"username": username, "iat": time.time()}
    payload = encrypt(payload)
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    cache.set(username, token, TIME_OUT)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


def get_username(token):
    payload = get_payload(token)
    return payload['username']


def check_token(token):
    username = get_username(token)
    last_token = cache.get(username)
    if last_token:
        return last_token == token
    return False


def user_check(username, password):
    try:
        user = User.objects.get(user_name=username)
    except User.DoesNotExist:
        return None
    if user:
        if user.user_password == base64.encodestring(password):
            return True
    return False

