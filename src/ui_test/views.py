# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.decorators import user_required

def show_template(request, template):
	return render_to_response(template+".html", context_instance=RequestContext(request))
