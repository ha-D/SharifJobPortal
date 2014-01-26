from django import template
from social_network.models import Message

register = template.Library()

@register.filter
def unreadMessagesCount(value):
    res = Message.objects.filter(reciever = value, unread = True).count()
    return res
#    return type('IntegerWrapper', (template.Node,), {'n': res, 'render': (lambda self: self.n)})
