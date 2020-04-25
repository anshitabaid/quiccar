from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .constants import *



class SignUpForm(UserCreationForm):
    number = forms.CharField (max_length = 10, validators = [PHONENUMBER_VALIDATOR])

    def __init__ (self, *args, **kwargs):
        super (UserCreationForm, self).__init__ (*args, **kwargs)
        self.fields['email'].required = True
        self.fields ['first_name'].required = True
        self.fields ['last_name'].required =True

    class Meta:
        model = User
        fields = ('username', 'number', 'email', 'password1', 'password2', 'first_name', 'last_name' )
        
    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit = False)
        user.number=self.cleaned_data["number"]
        if commit:
            user.save()
        return user