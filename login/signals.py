from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import infor,userpreferance
from .views import randomizer
from random import randint

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        a = infor(user=instance)
        a.slug = instance.username
        a.passwordkey = randomizer()
        a.save()
        a = userpreferance(user = instance)
        a.save()
