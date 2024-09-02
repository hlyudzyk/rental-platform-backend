from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Reservation
from django.conf import settings


@receiver(post_save, sender=Reservation)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        property_owner = instance.property.host

        context = {
            'user': property_owner,
            'property': instance.property,
            'reservation': instance,
            'booking_url': f"{settings.WEBSITE_URL}/properties/{instance.property.id}"
        }


        html_content = render_to_string('emails/booking_confirmation.html', context)
        text_content = strip_tags(html_content)  # Fallback plain text version

        subject = 'Your property has been booked!'
        from_email = 'valerijglud0@gmail.com'
        recipient = property_owner.email

        email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
        email.attach_alternative(html_content, "text/html")  # Attach the HTML version

        email.send()

