from django.http.response import HttpResponseRedirect
from utils.functions 		import template
def index(request):
    return HttpResponseRedirect('/home/')

def home(request):
    return template(request, 'home.html')