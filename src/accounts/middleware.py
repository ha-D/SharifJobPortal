from accounts.models import JobSeeker, Employer

class UserMiddleware:
    def process_request(self, request):
		try:
			if request.user.is_authenticated():# and not request.user.is_superuser:
				try:
					userprofile = JobSeeker.objects.get(user = request.user)
				except:
					try:
						userprofile = Employer.objects.get(user = request.user)
					except:
						userprofile = None

				request.userprofile = userprofile
		except:
			pass
		return None