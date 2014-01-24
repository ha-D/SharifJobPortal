from social_network.models         import *
from django.contrib import admin

admin.site.register(Message)
admin.site.register(CommentOnOpportunity)
admin.site.register(CommentOnEmployer)
admin.site.register(RateForOpportunity)
admin.site.register(RateForEmployer)
admin.site.register(FriendShip)
admin.site.register(Event_CommentOnEmployer)
admin.site.register(Event_CommentOnOpportunity)
admin.site.register(Event_FriendShip)

