from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from accounts.models import Employer, JobSeeker

def user_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def employer_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        elif not instanceof(request.user.userprofile, Employer):
            raise Http404
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def jobseeker_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        elif not instanceof(request.user.userprofile, JobSeeker):
            raise Http404
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap