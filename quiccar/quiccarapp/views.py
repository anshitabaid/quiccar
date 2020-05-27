from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from http import HTTPStatus
import json, re, datetime
from .models import *
from .helpers import *
from .constants import *
from geolib import geohash
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import make_aware


def index (request):
    return sendResponse (True, "Hello")


def pleaseLogin (request):
    return sendResponse (False, "Please login")
'''
@csrf_exempt    
def signup(request):
    if request.method == 'POST':
        data = json.loads (request.body)
        #
        if isDataValid (data['number'], data['email'], data['firstname'], data['lastname']):
            if (User.objects.filter(number = data['number'])):
                return HttpResponse ("Duplicate phone number")
            user = User ()
            user.createObject (data)
            try:
                user.full_clean()
            raise Exception as e:
                return HttpResponse ("Data not clean")
        #
        user = User()
        user.createObject(data)
        try:
            user.full_clean()
            user.save()
            return HttpResponse ("Ok")
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
def signin (request):
    if request.method == 'POST':
        data=json.loads (request.body)
        number=data['number']
        password = data['password']
        if (isNumberValid (number)==False):
            return HttpResponse ("Invalid number")
        user = User.objects.filter (number = number)
        print (user)
        if user:
            encoded_pass = user[0].password
            if check_password (password, encoded_pass):
                return HttpResponse ("Ok")
        return HttpResponse ("Invalid username or password")
'''

'''
@csrf_exempt
def insertRide (request):
    if request.method=='GET':
        if request.user.is_authenticated:
            data = request.GET.dict()
            data['user'] = request.user
            ride = Ride.objects.create (**data)
            ride.startHash = geohash.encode (float(ride.startX), float(ride.startY), PRECISION+1)
            ride.endHash = geohash.encode (float(ride.endX), float(ride.endY), PRECISION+1)
            try:
                ride.full_clean()
                ride.save()
                return HttpResponse("Ok")
            except Exception as e:
                return HttpResponse (e)
        else:
            return HttpResponse ("User not logged in")
'''
