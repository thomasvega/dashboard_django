from django.forms import ModelForm
from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # if we want only specific field from models : ['customer', 'product']
        
