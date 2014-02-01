from django.http.response import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect('/home')