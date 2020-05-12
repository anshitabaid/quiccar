from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from http import HTTPStatus
import json, re
from .models import Ride
from .helpers import *
from .constants import *
from geolib import geohash
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.forms.models import model_to_dict
# Create your views here.


def index (request):
    return HttpResponse ("Hello")

@csrf_exempt
def signup (request):
    form = SignUpForm (request.POST)
    if  form.is_valid():
        user = form.save ()
        user.refresh_from_db
        user.profile.number=form.cleaned_data.get('number')
        #user.profile.firstname = form.cleaned_data.get('firstname')
        #user.profile.lastname = form.cleaned_data.get('lastname')
        #user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        #user = authenticate (username=username, password = password)
        login (request, user)
        return sendResponse (True, None)
    return sendResponse (False, form.errors)

@csrf_exempt
def signin (request):
    username = request.POST ['username']
    password = request.POST ['password']
    user = authenticate (request, username = username, password = password)
    if  user is not None:
        login(request, user)
        return sendResponse (True, user)
    else:
        return sendResponse (False, "Unable to authenticate")

@csrf_exempt
def signout (request):
    logout (request)
    return sendResponse (True, None)

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

@csrf_exempt
@login_required
def insertRide (request):
    if request.method=='GET':
        data = request.GET.dict()
        data['user'] = request.user
        ride = Ride(**data)
        try:
            ride.full_clean()
        except Exception as e:
            return sendResponse (False, e)
        ride.startHash = geohash.encode (float(ride.startX), float(ride.startY), PRECISION+1)
        ride.endHash = geohash.encode (float(ride.endX), float(ride.endY), PRECISION+1)
        ride.save()
        return sendResponse(True, None)
        
    

#filter by user
@csrf_exempt
def viewRidesByUser (request):
        username = request.GET['username']
        rides = Ride.objects.filter (user__username = username)
        qs_json = serializers.serialize('json', rides)
        return sendResponse(True, qs_json ) #, content_type='application/json')
'''
@login_required
@csrf_exempt
def searchRides (request):
    if request.method=='GET':
        ride = Ride.objects.create (**request.GET.dict())
        ride.startHash = geohash.encode (float(ride.startX), float(ride.startY), PRECISION)
        ride.endHash = geohash.encode (float(ride.endX), float(ride.endY), PRECISION)

        #Neighbouring geohash blocks for start and end points
        startNeighbours = findNeighbours (ride.startHash)
        endNeighbours = findNeighbours (ride.endHash)

        #slice first PRECISION-VARY_PREC no of characters from the hash for preliminary database search
        likeStartHash = ride.startHash[:PRECISION-VARY_PREC]
        likeEndHash = ride.endHash[:PRECISION-VARY_PREC]
        
        #generate regex string to match
        startRegex = makeRegex (startNeighbours)
        endRegex = makeRegex (endNeighbours) 
        
        try:
            ride.full_clean()
            #searching
            #queryRides = Ride.objects.all()
            queryRides = Ride.objects.filter (~Q(number=ride.number), startHash__startswith = likeStartHash, endHash__startswith = likeEndHash, isActive = True)
            queryRides = queryRides.filter (startHash__regex = startRegex, endHash__regex = endRegex)
            queryRidesJson = serializers.serialize ('json', queryRides)
            return HttpResponse (queryRidesJson, content_type = 'application/json')
        except Exception as e:
            return HttpResponse (e)
'''

@login_required
@csrf_exempt
def searchRides (request):
    if request.method=='GET':
        data = request.GET.dict()
        data['user'] = request.user
        ride = Ride(**data)
        try:
            ride.full_clean()
        except Exception as e:
            return sendResponse (False,e)
        ride.startHash = geohash.encode (float(ride.startX), float(ride.startY), PRECISION)
        ride.endHash = geohash.encode (float(ride.endX), float(ride.endY), PRECISION)

        #Neighbouring geohash blocks for start and end points
        startNeighbours = findNeighbours (ride.startHash)
        endNeighbours = findNeighbours (ride.endHash)

        #slice first PRECISION-VARY_PREC no of characters from the hash for preliminary database search
        likeStartHash = ride.startHash[:PRECISION-VARY_PREC]
        likeEndHash = ride.endHash[:PRECISION-VARY_PREC]
        
        #generate regex string to match
        startRegex = makeRegex (startNeighbours)
        endRegex = makeRegex (endNeighbours) 
        
        
        queryRides = Ride.objects.filter (~Q(user__username=ride.user.username), startHash__startswith = likeStartHash, endHash__startswith = likeEndHash, isActive = True)
        queryRides = queryRides.filter (startHash__regex = startRegex, endHash__regex = endRegex)
        queryRidesJson = serializers.serialize ('json', queryRides)
        return sendResponse (True, queryRidesJson)
            
