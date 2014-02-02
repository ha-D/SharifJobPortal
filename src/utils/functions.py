__author__ = 'Setareh'

from django.http 				import HttpResponse
from django.shortcuts 			import render_to_response
from django.template.context 	import RequestContext
from django.template.loader		import render_to_string

import json

def template(request, address, context = {}):
    return render_to_response(address, RequestContext(request, context))

def json_response(response):
    return HttpResponse(json.dumps(response), content_type="application/json")

def ajax_template(request, address, context ={}):
    return json_response({
        "result": 1,
        "data": render_to_string(address, RequestContext(request, context))
    })

