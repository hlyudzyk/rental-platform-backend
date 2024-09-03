from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reservation
from .tasks import booking_confirmed


@receiver(post_save, sender=Reservation)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        booking_confirmed.delay(instance.id)

