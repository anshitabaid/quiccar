import re, json, random, string
from geolib import geohash
from .constants import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet


def isEmailValid (email):
    if (re.match (r"^[A-Za-z0-9._%+-]+\@[a-zA-Z0-9]+\.[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?$", email)) is None:
        return False
    else:
        return True


def isNumberValid (phone):
    if (re.match(r"[0-9]{10}", phone)) is None:
        return False
    return True

def isNameValid (name):
    if (re.match (r"[a-zA-Z]+", name)) is None:
        return False
    return True

def isDataValid (phone, email, firstname, lastname):
    
    #return (isPhoneValid(phone) and isEmailValid(email) and isNameValid(firstname) and isNameValid(lastname))
    if not isPhoneValid (phone):
        print (phone)
        return False
    if not isEmailValid (email):
        print (email)
        return False
    if not isNameValid(firstname):
        print (firstname)
        return False
    if not isNameValid (lastname):
        print (lastname)
        return False
    return True

def makeRegex(nbr):
    '''
    neighbours=nbr
    base = '(.....{})'
    rgx = ''
    l = len(neighbours)
    print (l)
    for i in range (l-1):
        rgx = rgx + base.format (neighbours[i][-VARY_PREC]) + '|'
    rgx = rgx + base.format (neighbours[l-1][-VARY_PREC])
    rgx = '^(' + rgx +')'
    print (rgx)
    '''
    
    rgx = '^((.....{})|(.....{})|(.....{})|(.....{})|(.....{})|(.....{})|(.....{})|(.....{})|(.....{}))'.format (
        nbr[0][-VARY_PREC], nbr[1][-VARY_PREC], nbr[2][-VARY_PREC], nbr[3][-VARY_PREC], 
        nbr[4][-VARY_PREC], nbr[5][-VARY_PREC], nbr[6][-VARY_PREC], nbr[7][-VARY_PREC], nbr[8][-VARY_PREC]
    )
    return rgx

def findNeighbours (hash):
    neighbours = list(geohash.neighbours(hash))
    neighbours.append (hash)
    return neighbours

def converter(obj):
    ret = {}
    if isinstance (obj, ValidationError):
        for key, value in obj:
            ret[key] = value
        return ret
    if isinstance (obj, User):
        ret['username']=obj.username
        ret['first_name']=obj.first_name
        ret['last_name']=obj.last_name
        ret['email']=obj.email
        ret['number']=obj.profile.number
        return ret

    return None
'''
def userDict (user):
    u={}
    u['username']=user.username
    u['firstname']=user.first_name
    u['lastname']=user.last_name
    u['email']=user.email
    u['phone']=user.profile.number
    return u
'''
def sendResponse (success, message):
    response = {}
    response['success']=success
    if success:
        response['message']=message
    else:
        response['error']=message
    return HttpResponse (json.dumps (response, default = converter),  content_type = 'application/json')


def makeToken ():
    characters=string.ascii_letters+string.digits
    return ''.join((random.choice(characters) for i in range(TOKEN_LENGTH)))


def parseRides(queryRides):
    l = []
    for qr in queryRides:
        d={}
        d['pk']=qr.pk
        d['first_name']=qr.user.get_short_name()
        d['last_name']=qr.user.last_name
        d['number']=qr.user.profile.number
        d['email']=qr.user.email
        d['startX']=str(qr.startX)
        d['startY']=str(qr.startY)
        d['endX']=str(qr.endX)
        d['endY']=str(qr.endY)
        d['startAddress']=qr.startAddress
        d['endAddress']=qr.endAddress
        d['time']=qr.time.strftime(DATETIME_FORMAT)
        d['capacity']=qr.capacity
        l.append (d)
    return l
