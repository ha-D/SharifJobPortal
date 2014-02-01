from django.views.decorators.csrf   import csrf_exempt
from utils.functions1 	import json_response
from markdown import markdown


@csrf_exempt
def zedit_preview(request):
	content = request.POST.get('content', '')
	return json_response({'result': 'success', 'content': markdown(content)})