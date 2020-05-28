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
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import make_aware
from .views import *

@csrf_exempt
def verifyEmail(request):
    if request.method=='GET':
        email = request.GET.dict()['email']
        if User.objects.filter (email = email).exists ():
            return sendResponse(False, 'Email already in use')
        token = makeToken(EV_TOKEN_LENGTH)
        emailToken = EmailToken()
        emailToken.email = email
        emailToken.token = token
        try:
            emailToken.full_clean()
        except ValidationError:
            return sendResponse (False, 'Validation Error')
        emailToken.save()
        return sendResponse(True, None)
    
    elif request.method == 'POST':
        data = request.POST
        print (data)
        try:
            emailToken = EmailToken.objects.get (email = data['email'], token = data['token'])
            emailToken.delete()
            return sendResponse (True, None)
        except Exception:
            return sendResponse (False, 'Incorrect email or token')


    
    

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


#@csrf_exempt
def registerToken (request):
    if request.method=='GET':
        data = request.GET.dict()
        try:
            entry = User.objects.get (username = data['username'])
        except Exception as e:
            return sendResponse(False, 'Username does not exist')
        pr = PasswordReset (**data)
        pr.token = makeToken(FP_TOKEN_LENGTH)
        #Prepare email body
        link= CHANGE_PASSWORD_LINK.format (username=entry.username, token=pr.token)
        body = EMAIL_BODY.format (name = entry.get_short_name(), link = link)
        print (link)
        try:
            send_mail(EMAIL_SUBJECT,body, settings.EMAIL_HOST_USER, [entry.email], fail_silently=False)   
        except Exception as e:
            return sendResponse(False, 'Mail not sent')
        pr.save()        
        return sendResponse(True, None)
    return sendResponse(False, 'Incorrect method')

@csrf_exempt
def verifyToken (request):
    #Route to redirect to form for password reset
    if request.method == 'GET':
        data=request.GET.dict()
        try:
            entry = PasswordReset.objects.get (username = data['username'], token = data['token'])
            now = datetime.datetime.now (TIMEZONE)
            if (now-entry.added).total_seconds() > LINK_VALID_TIME*60*60:
                #if link is older than 12 hours
                entry.delete()
                raise Exception ()
        except Exception as e:
            return render (request, 'password_reset.html', {'flag':False})
        now = datetime.datetime.now(TIMEZONE)
        return render (request, 'password_reset.html', {'flag':True, 'username':entry.username, 'token': entry.token})

    #new password form
    elif request.method=='POST':
        data = request.POST
        if data['password1']!=data['password2']:
            return render (request, 'password_reset.html', {'flag': True, 'message':'Both passwords should match', 'username': data['username'], 'token':data['token']})
        #retrieve token object from database
        try:
            entry = PasswordReset.objects.get (username = data['username'], token = data['token'])
        except Exception as e:
            return HttpResponse('Invalid link')
        try:
            #find user and update the password
            user = User.objects.get (username = data['username'])
            user.set_password(data['password1'])
            user.save()
            #delete token entry
            entry.delete()
        except Exception as e:
            print (e)
            return render (request, 'password_reset.html',{'flag':True, 'message':'Invalid password', 'username':data['username'], 'token': data['token']})
        
        return HttpResponse('Password reset successful!')
        
    else:
        return sendResponse(False, 'Incorrect method')
