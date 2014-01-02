class UserMiddleware:
    def process_request(self, request):
		try:
			if request.user.is_authenticated():# and not request.user.is_superuser:
				profile = request.user.userprofile
				request.userprofile = profile
		except:
			pass
		return None