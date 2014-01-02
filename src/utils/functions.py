from django.shortcuts import render_to_response
from django.template.context import RequestContext

import json

def template(request, address, context = {}):
	return render_to_response(address, RequestContext(request, context))

def json_response(response):
    return HttpResponse(json.dumps(response))
