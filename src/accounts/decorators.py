from django.contrib.auth.views  import redirect_to_login
from django.http                import Http404
from accounts.models            import Employer, JobSeeker
from utils.functions            import json_response
from django.conf                import settings

def user_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def user_required_ajax(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return json_response({"result":0, "error":"unauthorized", "data":settings.LOGIN_URL})
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def employer_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        elif not request.userprofile.is_employer():
            return redirect_to_login(request.get_full_path())
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def jobseeker_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        elif not request.user.userprofile.is_jobseeker():
            return redirect_to_login(request.get_full_path())
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap