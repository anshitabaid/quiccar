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
from django.utils.timezone import localtime 

@csrf_exempt
@login_required
def insertRide (request):
    if request.method=='GET':
        data = request.GET.dict()
        data['user'] = request.user
        data['isActive']=True
        ride = Ride(**data)
        try:
            ride.full_clean()
        except Exception as e:
            return sendResponse (False, e)
        ride.startHash = geohash.encode (float(ride.startX), float(ride.startY), PRECISION+1)
        ride.endHash = geohash.encode (float(ride.endX), float(ride.endY), PRECISION+1)
        ride.time = make_aware(ride.time)
        ride.save()
        return sendResponse(True, None)
        
    

#filter by user
@csrf_exempt
def viewRidesByUser (request):
    if request.method=='GET':
        username = request.GET['username']
        queryRides = Ride.objects.filter (user__username = username).order_by('-time')
        for q in queryRides:
            q.time=localtime(q.time)
        queryRides = parseRides (queryRides)
        #qs_json = serializers.serialize('json', rides)
        return sendResponse(True, queryRides )

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

        #also include rides from upto MINUTES_CUTOFF minutes ago
        ride.time = make_aware(ride.time)-datetime.timedelta(minutes=MINUTES_CUTOFF)
        

        #Neighbouring geohash blocks for start and end points
        startNeighbours = findNeighbours (ride.startHash)
        endNeighbours = findNeighbours (ride.endHash)

        #slice first PRECISION-VARY_PREC no of characters from the hash for preliminary database search
        likeStartHash = ride.startHash[:PRECISION-VARY_PREC]
        likeEndHash = ride.endHash[:PRECISION-VARY_PREC]
        
        #generate regex string to match
        startRegex = makeRegex (startNeighbours)
        endRegex = makeRegex (endNeighbours) 
        
        queryRides = Ride.objects.filter (~Q(user__username=ride.user.username), startHash__startswith = likeStartHash, endHash__startswith = likeEndHash, isActive = True, time__gte = ride.time) 
        queryRides = queryRides.filter (startHash__regex = startRegex, endHash__regex = endRegex).order_by('time')
        
        for q in queryRides:
            q.time=localtime(q.time)

        queryRides = parseRides (queryRides)

        return sendResponse (True, queryRides)
    return sendResponse(False, 'Incorrect method')


@login_required
@csrf_exempt
def changeRideStatus (request):
    if request.method == 'GET':
        data = request.GET.dict()

        data['status']=data['status'].capitalize()
        query = Ride.objects.filter(pk = data['id'], user = request.user).first()
        if query is None:
            return sendResponse(False, 'Incorrect ride ID')
        now = make_aware(datetime.datetime.now())
        if data['status']=='True' and now > query.time:
            return sendResponse (False, 'Can\'t activate an old ride')
        query.isActive = data['status']
        query.save()
        return sendResponse (True, None)
    else:
        return sendResponse(False, 'Incorrect method')

