from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile, ProgressEntry


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=ProgressEntry)
def increment_verses_read(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.filter(user=instance.user).update(
            verses_read=F('verses_read') + 1
        )


@receiver(post_delete, sender=ProgressEntry)
def decrement_verses_read(sender, instance, **kwargs):
    UserProfile.objects.filter(user=instance.user, verses_read__gt=0).update(
        verses_read=F('verses_read') - 1
    )
