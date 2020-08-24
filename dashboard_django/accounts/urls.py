from django.urls import path
from . import views 

"""
    In this file we add all url that link into views.
    urlpatterns is a list.
    path is a method from django.urls
    We specify the path then the view (that is a method) then the name of the path.
"""

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    
    path('products/', views.products, name="products"),
    
    path('customer/<str:pk>/', views.customer, name="customer"),
    
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
