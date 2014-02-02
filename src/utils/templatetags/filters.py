from django import template
from datetime import datetime, timedelta
from django.utils.safestring import SafeText
from SharifJobPortal.functions import to_persian_num
from SharifJobPortal.jDate import miladi2shamsi

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


## From Django-Widget-Tweaks  ##

def _process_field_attributes(field, attr, process):

    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        return old_as_widget(widget, attrs, only_initial)

    bound_method = type(old_as_widget)
    try:
        field.as_widget = bound_method(as_widget, field, field.__class__)
    except TypeError:  # python 3
        field.as_widget = bound_method(as_widget, field)
    return field

@register.filter("append_attr")
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value
    return _process_field_attributes(field, attr, process)


@register.filter("addclass")
def addclass(field, css_class):
    return append_attr(field, 'class:' + css_class)
