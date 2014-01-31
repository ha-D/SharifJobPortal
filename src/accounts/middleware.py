from accounts.models import JobSeeker, Employer

class UserMiddleware:
    def process_request(self, request):
		try:
			if request.user.is_authenticated():# and not request.user.is_superuser:
				request.has_profile = True
				try:
					userprofile = JobSeeker.objects.get(user = request.user)
				except:
					try:
						userprofile = Employer.objects.get(user = request.user)
					except:
						userprofile = None
						request.has_profile = False

				request.user.userprofile = userprofile
				request.userprofile = userprofile
		except:
			request.has_profile = False

		return None