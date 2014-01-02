class UserMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated(): # and not request.user.is_superuser:
            profile = request.user.userprofile
            request.userprofile = profile
        return None