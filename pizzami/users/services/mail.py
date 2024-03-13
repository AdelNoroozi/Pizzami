from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.settings.email_sending import EMAIL_HOST
from pizzami.core.constants import BASE_URL
from pizzami.users.models import BaseUser


def send_welcome_mail(user: BaseUser, public_name: str):
    subject = "Welcome to Pizzami!"
    message = f"Hello {public_name}. Welcome to Pizzami.\nWish you a great day."
    recipients = [user.email]
    try:
        send_mail(subject=subject, message=message, from_email=EMAIL_HOST, recipient_list=recipients)
    except:
        pass


def request_password_reset(email: str) -> bool:
    user = BaseUser.objects.filter(email=email).first()
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    link = f"{BASE_URL.restrip('/')}/api/user/reset-password/{uid}/{token}/"
    subject = "Password Reset"
    message = f"use this link to reset your password:\n{link}\nif you have not requested for password reset, ignore " \
              f"this message."
    recipients = [email]
    try:
        send_mail(subject=subject, message=message, from_email=EMAIL_HOST, recipient_list=recipients)
    except:
        return False
    return True

