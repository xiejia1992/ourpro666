# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from models import User
from serializer import UserSerializer
from django.shortcuts import render_to_response
from api_method import get_model_list, add_model, get_model_id, put_model_id, delete_model_id

# Create your views here.


def login(request):
    return render_to_response('login.html')


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        return get_model_list(request=request,
                              Model=User,
                              Serializer=UserSerializer)
    elif request.method == 'POST':
        return add_model(request=request,
                         Model=User,
                         Serializer=UserSerializer)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    if request.method == 'GET':
        return get_model_id(request=request,
                            id=id,
                            Model=User,
                            Serializer=UserSerializer)
    elif request.method == 'PUT':
        return put_model_id(request=request,
                            id=id, Model=User,
                            Serializer=UserSerializer)
