程序启动方式：
启动主程序
python manage.py runserver 0.0.0.0:8000
启动celery
celery -A ourpro worker --loglevel=INFO

====================================================================

API接口说明文档：

--------------------------------------------------------------------
api/check_register
#该接口检查用户是否在数据库中已经存在。
#如果不存在，则返回successful,并且发送验证码，验证码有效期为3分钟
#如果存在，则返回failed

method: POST

DATA: {
    "user": "xxxx"        #xxxx代表手机或者邮箱，手机或者邮箱格式需前端检查
    }

Response: successful
successful 根据手机或者邮箱的情况，返回两种结果
（1）手机验证码：
{
    "message": "The mobile identifying code send successfully",
    "status_code": 200
}
（2）邮箱验证码：
{
    "message": "The email identifying code send successfully",
    "status_code": 200
}

Response: failed
failed 返回一种结果
{
    "message": "The user already exists",
    "status_code": 409
}

--------------------------------------------------------------------
api/register
#该接口检查注册验证码是否过期，并将用户数据注册到数据库
#如果注册验证码未过期，则返回successful，并跳转值登陆页面
如果注册验证码已经过期，则返回failed

method: POST

DATA: {
    "user": "xxxx",                 #xxxx代表用户手机号或者邮箱帐号
    "password": "xxxx",             #xxxx代表用户密码，需前端验证只能是6-16位字符
    "identifying_code": "xxxx"      #xxxx代表手机或邮件收到的验证码
    }

Response: successful
successful 返回一种结果
{
    "message": "Register user successfully",
    "status_code": 200
}

Response: failed
failed 返回一种结果
{
    "message": "The identifying code expired",
    "status_code": 400
}


--------------------------------------------------------------------
api/login
#该接口验证用户帐号密码是否正确，用于用户登陆
#如果正确，则返回successful, 并跳转至首页
#如果不正确，则返回failed。

method: POST

DATA: {
    "user": "xxxx"              #代表用户登陆帐号，需前端验证只能是手机号或者邮箱
    "password": "xxxx",         #代表用户密码，需前端验证只能是6-16位字符
    }

Response: successful
successful 返回一种结果
{
    "user": "xxxx"
    "message": "xxxx",          #xxxx代表Token,需前端存储在本地，每次请求携带Token做验证
    "status_code": 200
}

Response: failed
failed 返回两种结果
（1）用户不存在
{
    "message": "The user was not found",
    "status_code": 404
}
（2) 用户登陆失败
{
    "message": "User login failed",
    "status_code": 403
}

--------------------------------------------------------------------
api/forget_password
#忘记密码接口，该接口验证用户是否存在
#如果用户存在，则返回successful, 并发送验证码
#如果不正确，则返回failed。

method: POST

DATA: {
    "user": "xxxx"              #代表用户登陆帐号，需前端验证只能是手机号或者邮箱
    }

Response: successful
successful 返回一种结果
{
    "message": "The identifying code send successfully",
    "status_code": 200
}

Response: failed
failed 返回1种结果
（1）用户不存在
{
    "message": "The user was not found",
    "status_code": 404
}

--------------------------------------------------------------------
api/reset_password
#忘记密码接口，该接口验证用户是否存在
#如果用户存在，则返回successful, 并发送验证码
#如果不正确，则返回failed。

method: POST

DATA: {
    "user": "xxxx",              #用户登陆帐号，需前端验证只能是手机号或者邮箱
    "identifying_code": "xxxxxx" #用户收到的6数字位验证码
    "new_password": "xxxx"       #用户新密码
    }

Response: successful
successful 返回一种结果
{
    "message": "The password has exchanged successfully",
    "status_code": 200
}

Response: failed
failed 返回1种结果
（1）用户不存在
{
    "message": "The identifying code expired",
    "status_code": 400
}

--------------------------------------------------------------------
