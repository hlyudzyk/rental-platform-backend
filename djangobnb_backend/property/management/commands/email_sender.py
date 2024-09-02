import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from useraccount.models import Reservation



class Command(BaseCommand):
    help = 'Sends an e-mail to users who recently booked properties'

    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int)


    def handle(self, *args, **options):
        emails = []
        reservations = Reservation.objects.filter(
            status=Reservation.Status.COMPLETED,
            feedback_email_sent=False
        )

        for reservation in reservations:
            subject = "Your opinion is important for us!"
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

        #send_mass_mail(emails)
        self.stdout.write(f"Sent {len(emails)} emails")
