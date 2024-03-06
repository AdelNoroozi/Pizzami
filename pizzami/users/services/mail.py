from django.core.mail import send_mail

from config.settings.email_sending import EMAIL_HOST
from pizzami.users.models import BaseUser


def send_welcome_mail(user: BaseUser, public_name: str):
    subject = "Welcome to Pizzami!"
    message = f"Hello {public_name}. Welcome to Pizzami.\nWish you a great day."
    recipients = [user.email]
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST, recipient_list=recipients)
