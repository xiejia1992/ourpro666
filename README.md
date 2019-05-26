API接口说明文档：

/register

method: POST

DATA: {
    "username": "username"
    "password": "password",
    }

Response: {
    "message": "Register user successfully",
    "status_code": 200
}


/login

method: POST

DATA: {
    "username": "username"
    "password": "password",
    }

Response: {
    "username": "username"
    "message": "Register user successfully",
    "status_code": 200
}