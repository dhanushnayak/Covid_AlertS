from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm 

class LoginForm(forms.Form):
    Email= forms.CharField(max_length = 100,)
    Password = forms.CharField()
    GroupId= forms.CharField()