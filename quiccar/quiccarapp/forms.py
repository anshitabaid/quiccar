from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .constants import *



class SignUpForm(UserCreationForm):
    number = forms.CharField (max_length = 10, validators = [PHONENUMBER_VALIDATOR])
    email = forms.EmailField(max_length=200, required=True)
    firstname = forms.CharField (max_length = 10, validators = [ALPHABET_VALIDATOR], required=True)
    lastname = forms.CharField (max_length= 10, validators = [ALPHABET_VALIDATOR], required=True)

    class Meta:
        model = User
        fields = ('username', 'number', 'email', 'password1', 'password2', 'firstname', 'lastname' )
    
    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit = False)
        user.email = self.cleaned_data["email"]
        user.number=self.cleaned_data["number"]
        if commit:
            user.save()
        return user