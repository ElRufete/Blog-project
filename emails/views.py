from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import UserActivationToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from www.settings import DEFAULT_FROM_EMAIL
import sendgrid
from sendgrid.helpers.mail import Mail
import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator

def get_sendgrid_client():
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        raise RuntimeError("Undefined SENDGRID_API_KEY")
    return sendgrid.SendGridAPIClient(api_key)
            


def welcome_email(request, user):
    """Utility function to send a welcome email with an activation link, 
    pass the newly created user as argument."""

    activate_token_generator = UserActivationToken()
    token = activate_token_generator.make_token(user)
    uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
    link_url = request.build_absolute_uri(
        reverse('accounts:activate_account', args=[uid_b64, token])
    )
    context = {'user_name': user.user_name,
               'uid_b64': uid_b64, 
               'token': token,
               'link_url': link_url,
               }
    welcome_email_html = render_to_string("emails/welcome_email.html",context)

    message = Mail(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails=[user.email],
        subject="Bienvenid@ a la blogoteca",
        html_content=welcome_email_html
    )

    sg = get_sendgrid_client()
    sg.send(message)
    


def reset_password_email(request, user):
    """Utility function to send an email with a reset password link,
    pass the user as argument"""

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
    link_url = request.build_absolute_uri(
        reverse('accounts:reset_password', args=[uid_b64, token])
    )
    context = {'user_name': user.user_name,
               'uid_b64': uid_b64, 
               'token': token,
               'link_url': link_url,
               }
    
    password_reset_email_html = render_to_string("emails/password_reset_email.html",context)
    message = Mail(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails=[user.email],
        subject="Restablecimiento de contraseña",
        html_content=password_reset_email_html
    )

    try:
        sg = get_sendgrid_client()
        response = sg.send(message)
        print("SENDGRID STATUS:", response.status_code)
        print("SENDGRID BODY:", response.body)
        print("SENDGRID HEADERS:", response.headers)
    except Exception as e:
        print("ERROR SENDGRID:", repr(e))
        raise
    


    
