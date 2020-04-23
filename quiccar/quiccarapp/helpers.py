import re
from geolib import geohash
from .constants import *
from django.http import HttpResponse

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
