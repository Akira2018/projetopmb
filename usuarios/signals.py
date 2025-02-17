#signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from usuarios.models import CustomUser

@receiver(post_save, sender=CustomUser)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='Gestores')  # Ou o grupo apropriado
        instance.groups.add(default_group)
