from django import template
from datetime import datetime, timedelta
from django.utils.safestring import SafeText
register = template.Library()

@register.filter(name='short_time')
def short_time(value):
	if value.date() == datetime.today().date():
		return value.strftime("%l:%M %p")
	elif value.date().year == datetime.today().year:
		return value.strftime("%b %d")
	else:
		return value.strftime("%b %d, %Y")

@register.filter(name='fullname')
def fullname(value):
	return '%s %s' % (value.first_name, value.last_name)

@register.filter(name='semfield')
def semfield(field):
	label = field.label_tag()
	inp = SafeText(field)
	err = ""
	if len(field.errors) > 0:
		err = '<div class="ui red pointing prompt label transition visible">%s</div>' % field.errors[0]

	if 'city' in label:
		print(type(inp))
	return SafeText("""
	<div class="small field">
		%s
		%s
		%s
	</div>
	""" % (label, inp, err))
	
@register.filter(name='jsbool')
def jsbool(field):
	if field == True:
		return 'true'
	elif field == False:
		return 'false'
	else:
		return ''