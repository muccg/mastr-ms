from functools import wraps
from django.utils.decorators import available_attrs
from django.http import *

def user_passes_test(test_func, response=None):
    """
    Decorator for views that checks that the user passes the given test,
    and returns the given response if necessary, HttpResponseForbidden(403) by default. 
    The test should be a callable that takes the user object and returns True if the user passes.
    The response must be a HttpResponse or subclass.
    Adapted from django.contrib.auth.decorators.user_passes_test
    """
    if not response or not isinstance(response, HttpResponse):
        response = HttpResponseForbidden()

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return response
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator
