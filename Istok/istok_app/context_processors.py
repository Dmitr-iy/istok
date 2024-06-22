from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = None
        return {'user_profile': profile}
    return {}
