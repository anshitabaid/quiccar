from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .constants import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

'''
class User (models.Model):
    number = models.CharField (max_length = 10, primary_key = True, unique = True, validators = [PHONENUMBER_VALIDATOR])
    password = models.CharField (max_length = 100)
    email = models.EmailField()
    firstname = models.CharField (max_length = 10, validators = [ALPHABET_VALIDATOR])
    lastname = models.CharField (max_length= 10, validators = [ALPHABET_VALIDATOR])
    def __str__ (self):
        return self.number
    
    def createObject(self, data):
        self.number = data['number']
        self.password =make_password(data['password'])
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
    #
    def clean (self):
        print (self.email)
        if (re.match (r"^[A-Za-z0-9._%+-]+\@[a-zA-Z0-9]+\.[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?$", self.email)) is None:
            print (self.email)
            raise ValidationError (_('Invalid email'))
        if (re.match(r"[0-9]{10}", self.number)) is None:
            raise ValidationError (_('Invalid number'))
        if (re.match (r"[a-zA-Z]+", self.firstname)) is None:
            raise ValidationError(_('Invalid name'))
        if (re.match (r"[a-zA-Z]+", self.lastname)) is None:
            raise ValidationError(_('Invalid name'))
    #
'''

class Ride (models.Model):
    number = models.CharField (max_length = 10,  validators = [PHONENUMBER_VALIDATOR])
    startX = models.DecimalField(max_digits=9, decimal_places=6)
    startY = models.DecimalField(max_digits=9, decimal_places=6)
    endX = models.DecimalField(max_digits=9, decimal_places=6)
    endY = models.DecimalField(max_digits=9, decimal_places=6)
    startHash = models.CharField(max_length = 12)
    endHash = models.CharField(max_length = 12)
    startAddress = models.CharField(max_length = 100)
    endAddress = models.CharField (max_length = 100)
    time  = models.DateTimeField ()
    capacity = models.IntegerField()
    isActive = models.BooleanField ()

    def __str__ (self):
        return self.number + ' ' + self.startHash + ' ' +self.endHash


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    number = models.CharField (max_length =10, validators =[PHONENUMBER_VALIDATOR])
    email = models.EmailField()
    firstname = models.CharField (max_length = 10, validators = [ALPHABET_VALIDATOR])
    lastname = models.CharField (max_length= 10, validators = [ALPHABET_VALIDATOR])

    def __str__ (self):
        return (self.user.username +" " + self.number )

@receiver (post_save, sender= User)
def create_user_profile (sender, instance, created, **kwargs):
    if created :
        Profile.objects.create (user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()