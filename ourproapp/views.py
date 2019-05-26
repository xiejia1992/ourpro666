# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import User
from serializer import UserSerializer, ResponseSerializer
from api_method import get_model_list, add_model, get_model_id, put_model_id, delete_model_id
from utils import create_token, user_check, check_token


# Create your views here.
@api_view(['POST'])
def register(request):
    username = request.data["username"]
    password = request.data["password"]
    if not username or not password:
        register_response = {'message': "username or password not exists", 'status_code': 400}
        return Response(ResponseSerializer(register_response).data)
    if User.objects.filter(user_name=username):
        register_response = {'message': "The user already exists", 'status_code': 409}
        return Response(ResponseSerializer(register_response).data)
    user = User.objects.create(
        user_name=username,
        user_password=base64.encodestring(password))
    user.save()
    register_response = {'message': "Register user successfully", 'status_code': 200}
    return Response(ResponseSerializer(register_response).data)



@api_view(['POST'])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    check_result = user_check(username, password)
    if check_result == True:
        token = create_token(username)
        login_response = {'message': token, 'status_code': 200}
        login_response = ResponseSerializer(login_response).data
        login_response["username"] = username
        return Response(login_response)
    elif check_result == None:
        login_response = {'message': "The user was not found", 'status_code': 404}
        return Response(ResponseSerializer(login_response).data)
    else:
        login_response = {'message': "User login failed", 'status_code': 403}
        return Response(ResponseSerializer(login_response).data)


@api_view(['GET'])
def user_list(request):
    if check_token(request.META['HTTP_AUTH']):
        return get_model_list(request=request,
                              Model=User,
                              Serializer=UserSerializer)
    else:
        response = {'message': "Token has expired", 'status_code': 403}
        return Response(ResponseSerializer(response).data)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    if check_token(request.META['HTTP_AUTH']):
        if request.method == 'GET':
            return get_model_id(request=request,
                                id=id,
                                Model=User,
                                Serializer=UserSerializer)
        elif request.method == 'PUT':
            return put_model_id(request=request,
                                id=id, Model=User,
                                Serializer=UserSerializer)
    else:
        response = {'message': "Token has expired", 'status_code': 403}
        return Response(ResponseSerializer(response).data)