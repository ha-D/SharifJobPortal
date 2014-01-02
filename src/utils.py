from django.shortcuts import render_to_response
from django.template.context import RequestContext

import json

def template(address, request):
    return render_to_response(address, context_instance=RequestContext(request))

def json_response(response):
    return HttpResponse(json.dumps(response))
