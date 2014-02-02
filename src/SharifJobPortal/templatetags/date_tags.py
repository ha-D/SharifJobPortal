import datetime
from django import template
from SharifJobPortal.functions import to_persian_num
from SharifJobPortal.jDate import miladi2shamsi

register = template.Library()

class JalaliDateNode(template.Node):
    def __init__(self, date=None):
        if date:
            self.date=template.Variable(date)
        else:
            self.date=None

    def render(self, context):
        if self.date:
            date=self.date.resolve(context)
        else:
            date=datetime.datetime.now()
        d= miladi2shamsi(date.month, date.day, date.year)
        return to_persian_num(d[2], 4)+"/"+to_persian_num(d[0])+"/"+to_persian_num(d[1])

class PersianTimeNode(template.Node):
    def __init__(self, date):
        self.date=template.Variable(date)

    def render(self, context):
        date=self.date.resolve(context)
        return to_persian_num(date.hour, 2)+":"+to_persian_num(date.minute)+":"+to_persian_num(date.second)


@register.tag
def get_jalali_date(parser, token):
    tag_name, date = token.split_contents()

    return JalaliDateNode(date)

@register.tag
def get_now_jalali_date(parser, token):
    return JalaliDateNode()

@register.tag
def get_persian_time(parser, token):
    tag_name, date = token.split_contents()

    return PersianTimeNode(date)
