from .models import Verse, UserProfile


def reading_progress(request):
    if not request.user.is_authenticated:
        return {'reading_progress': 0}

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    total_verses = Verse.objects.count()
    progress = (profile.verses_read / total_verses * 100) if total_verses else 0
    return {'reading_progress': progress}
