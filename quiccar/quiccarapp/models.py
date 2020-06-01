from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .constants import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


User._meta.get_field('email')._unique = True



class Ride (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True)    
    startX = models.DecimalField(max_digits=9, decimal_places=6)
    startY = models.DecimalField(max_digits=9, decimal_places=6)
    endX = models.DecimalField(max_digits=9, decimal_places=6)
    endY = models.DecimalField(max_digits=9, decimal_places=6)
    startHash = models.CharField(db_index = True, max_length = 12, blank = True, null=True)
    endHash = models.CharField(db_index = True, max_length = 12, blank = True, null=True)
    startAddress = models.CharField(max_length = 100,blank = True)
    endAddress = models.CharField (max_length = 100, blank = True)
    time  = models.DateTimeField ()
    capacity = models.IntegerField()
    isActive = models.BooleanField (blank = True)

    def __str__ (self):
        return self.user.profile.number + ' ' + self.startAddress + ' ' +self.endAddress

    
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    number = models.CharField (max_length =10, validators =[PHONENUMBER_VALIDATOR])

    def __str__ (self):
        return (self.user.username +" " + self.number )

@receiver (post_save, sender= User)
def create_user_profile (sender, instance, created, **kwargs):
    if created :
        Profile.objects.create (user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PasswordReset (models.Model):
    username = models.CharField (max_length=150, primary_key = True)
    token = models.CharField (max_length=FP_TOKEN_LENGTH)
    added =models.DateTimeField (auto_now= True, null = True )

    def __str__ (self):
        return self.username

class EmailToken (models.Model):
    email = models.EmailField ()
    token = models.CharField (max_length=EV_TOKEN_LENGTH)
    def __str__ (self):
        return self.email