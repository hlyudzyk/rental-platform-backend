from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from .models import Reservation
from django.conf import settings


@shared_task
def booking_confirmed(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    property_owner = reservation.property.host

    context = {
        'user': property_owner,
        'property': reservation.property,
        'reservation': reservation,
        'booking_url': f"{settings.WEBSITE_URL}/properties/{reservation.property.id}"
    }

    html_content = render_to_string('emails/booking_confirmation.html', context)
    text_content = strip_tags(html_content)  # Fallback plain text version

    subject = 'Your property has been booked!'
    from_email = settings.EMAIL_HOST_USER
    recipient = property_owner.email

    email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
    email.attach_alternative(html_content, "text/html")  # Attach the HTML version

    email.send()

@shared_task
def email_feedback_reminder():
    emails = []
    reservations = Reservation.objects.filter(
        status=Reservation.Status.PENDING,
        feedback_email_sent=False
    )

    subject = "Your opinion is important for us!"

    for reservation in reservations:
        receiver = reservation.created_by
        message = f"""Dear {receiver.name},
        Recently you booked this property. Leave us know what you think!
        """
        emails.append((subject,
                      message,
                      settings.DEFAULT_FROM_EMAIL,
                      [receiver.email]
                    )
        )

        reservation.feedback_email_sent = True
        reservation.save()

    send_mass_mail(emails)
