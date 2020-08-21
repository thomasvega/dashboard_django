from django.contrib import admin

# Register your models here.
from .models import *

"""
    This file is needed to register the model inside the admin page
    It will allow us to add, remove, update data directly inside the admin page.
"""

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)