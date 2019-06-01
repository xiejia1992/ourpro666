# -*- coding: utf-8 -*-
#sender identifying code by email or mobile


import sys
import smtplib
import requests
import random
from django.core.cache import cache
from celery import shared_task
from email.mime.text import MIMEText
from ourpro_config import email_password, mobile_api_key
reload(sys)
sys.setdefaultencoding('utf-8')


@shared_task
def sender_identifying_code_to_email(user_email):
    identifying_code = str(random.randint(000000, 999999))
    _TIME_OUT = 3 * 60
    cache.set(user_email + "_identifying_code", identifying_code, _TIME_OUT)
    _from_user = "843359825@qq.com"
    _pwd = email_password
    msg = MIMEText(user_email + " ，您好: \n" + "    您的注册码为: " + identifying_code + \
                   " 该验证码在3分钟内有效，请及时注册", 'plain', 'utf-8')
    msg["Subject"] = unicode("[ourpro666] 注册验证码", 'utf-8')
    msg["From"] = _from_user
    msg["To"] = user_email
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(_from_user, _pwd)
    s.sendmail(_from_user, user_email, msg.as_string())
    s.quit()


@shared_task
def sender_identifying_code_to_mobile(user_mobile):
    identifying_code = str(random.randint(000000, 999999))
    _TIME_OUT = 3 * 60
    cache.set(user_mobile + "_identifying_code", identifying_code, _TIME_OUT)
    _api_key = mobile_api_key
    _yunpian_url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    parmas = {
        'apikey': _api_key,
        'mobile': user_mobile,
        'text': '【ourpro测试】您的验证码是' + identifying_code + '。如非本人操作，请忽略本短信'
    }
    requests.post(_yunpian_url, data=parmas)
