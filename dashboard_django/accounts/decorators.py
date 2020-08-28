from django.http import HttpResponse
from django.shortcuts import redirect

"""
Example for loginPage function :
    view_func become loginPage function
    we call unauthenticated_user first, do some check then return wrapper_func
"""

def unauthenticated_user(view_func):
    """
        Decorator to check if the user is authenticated,
        if so, we redirect hime through home page
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('Wrapper working', allowed_roles)

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator
