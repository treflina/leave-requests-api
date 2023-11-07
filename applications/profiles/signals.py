import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from applications.profiles.models import EmployeeProfile
from empportal.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)
        logger.info(f"{instance}'s contract details has been created.")
