from django.contrib.auth.models import User
from .models import Profil
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(staff = instance)
    else:
        instance.profil.save()

