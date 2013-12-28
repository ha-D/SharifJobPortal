from django.shortcuts import render_to_response
from django.template.context import RequestContext

def template(address, request):
    return render_to_response(address, context_instance=RequestContext(request))