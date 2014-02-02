from django.db.models.query_utils import Q
from accounts.models 		import JobSeeker
from social_network.models 	import *


'''
	Returns True if the jobseekers are friends	
'''
def friends(jobseeker1, jobseeker2):
    if list(FriendShip.objects.filter(Q(jobSeeker1=jobseeker1)& Q(jobSeeker2=jobseeker2) & Q(status=FriendShip.ACCEPTED))):
        return True
    if list(FriendShip.objects.filter(Q(jobSeeker2=jobseeker1)& Q(jobSeeker1=jobseeker2) & Q(status=FriendShip.ACCEPTED))):
        return True
    return False
