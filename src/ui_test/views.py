# Create your views here.
from django.shortcuts import render_to_response

def show_template(request, template):
	return render_to_response(template+".html")
