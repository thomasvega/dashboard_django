from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

"""
    This file is used to create specific form
    We can change the fields if want specific  input and not all input check createUserForm for a better understanding
"""

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # if we want only specific field from models : ['customer', 'product']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
