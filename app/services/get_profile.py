from app.models.profile import Profile

def get_profile_by_id(user_id):
    profile = Profile.objects.filter(id=user_id).first()
    return profile