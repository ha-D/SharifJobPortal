from django import template
from datetime import datetime, timedelta

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