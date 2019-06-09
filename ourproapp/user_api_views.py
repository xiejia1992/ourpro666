# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import User
from serializer import UserSerializer, ResponseSerializer
from api_method import get_model_list, add_model, get_model_id, put_model_id, delete_model_id
from .tasks import sender_identifying_code_to_email, sender_identifying_code_to_mobile
from utils import create_token, check_user_login, check_token, check_user_exists, check_register_code


# Create your views here.
@api_view(['POST'])
def check_register(request):
    user = request.data["user"]
    if check_user_exists(user):
        register_identifying_response = {'message': "The user already exists", 'status_code': 409}
        return Response(ResponseSerializer(register_identifying_response).data)
    else:
        if len(user) == 11 and '@' not in user:
            sender_identifying_code_to_mobile.delay(user)
            register_identifying_response = {'message': "The identifying code send successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_identifying_response).data)
        else:
            sender_identifying_code_to_email.delay(user)
            register_identifying_response = {'message': "The identifying code send successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_identifying_response).data)


@api_view(['POST'])
def register(request):
    user, password, identifying_code = request.data["user"], request.data["password"], request.data["identifying_code"]
    if check_register_code(user, identifying_code):
        if "@" in user:
            user = User.objects.create(
                user_mobile='',
                user_email=user,
                user_password=base64.encodestring(password)
            )
            user.save()
            register_response = {'message': "Register user successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_response).data)
        else:
            user = User.objects.create(
                user_mobile=user,
                user_email='',
                user_password=base64.encodestring(password)
            )
            user.save()
            register_response = {'message': "Register user successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_response).data)
    else:
        register_response = {'message': "The identifying code expired", 'status_code': 400}
        return Response(ResponseSerializer(register_response).data)


@api_view(['POST'])
def forget_password(request):
    user = request.data["user"]
    if check_user_exists(user):
        if len(user) == 11 and '@' not in user:
            sender_identifying_code_to_mobile.delay(user)
            register_identifying_response = {'message': "The mobile identifying code send successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_identifying_response).data)
        else:
            sender_identifying_code_to_email.delay(user)
            register_identifying_response = {'message': "The email identifying code send successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_identifying_response).data)
    register_identifying_response = {'message': "The user not found", 'status_code': 404}
    return Response(ResponseSerializer(register_identifying_response).data)


@api_view(['POST'])
def reset_password(request):
    user, identifying_code, new_password = request.data["user"], request.data["identifying_code"], request.data["new_password"]
    if check_register_code(user, identifying_code):
        if "@" in user:
            user = User.objects.get(user_email=user)
            user.user_password = base64.encodestring(new_password)
            user.save()
            register_response = {'message': "Reset password successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_response).data)
        else:
            user = User.objects.get(user_mobile=user)
            user.user_password = base64.encodestring(new_password)
            user.save()
            register_response = {'message': "Reset password successfully", 'status_code': 200}
            return Response(ResponseSerializer(register_response).data)
    else:
        register_response = {'message': "The identifying code expired", 'status_code': 400}
        return Response(ResponseSerializer(register_response).data)


@api_view(['POST'])
def login(request):
    user, password = request.data["user"], request.data["password"]
    check_result = check_user_login(user, password)
    if check_result is True:
        token = create_token(user)
        login_response = {'message': token, 'status_code': 200}
        login_response = ResponseSerializer(login_response).data
        login_response["user"] = user
        return Response(login_response)
    elif check_result is None:
        login_response = {'message': "The user was not found", 'status_code': 404}
        return Response(ResponseSerializer(login_response).data)
    else:
        login_response = {'message': "User login failed", 'status_code': 403}
        return Response(ResponseSerializer(login_response).data)


@api_view(['GET'])
@check_token
def user_list(request):
    return get_model_list(request=request,
                          Model=User,
                          Serializer=UserSerializer)


# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, id):
#     if check_token(request.META['HTTP_AUTH']):
#         if request.method == 'GET':
#             return get_model_id(request=request,
#                                 id=id,
#                                 Model=User,
#                                 Serializer=UserSerializer)
#         elif request.method == 'PUT':
#             return put_model_id(request=request,
#                                 id=id, Model=User,
#                                 Serializer=UserSerializer)
#     else:
#         response = {'message': "Token has expired", 'status_code': 403}
#         return Response(ResponseSerializer(response).data)