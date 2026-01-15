from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import UserActivationToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.conf import settings

User = settings.AUTH_USER_MODEL
default_from_email = 'no-reply@blogotecaderufo.es'

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
    welcome_email_content = strip_tags(welcome_email_html)
    email = EmailMultiAlternatives(
        subject=f'¡Bienvenid@ a la blogoteca, {user.user_name}!',
        body=welcome_email_content,
        from_email=default_from_email,
        to=[user.email]
    )

    email.attach_alternative(welcome_email_html,"text/html")
    email.send(fail_silently=True)

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
    password_reset_email_content = strip_tags(password_reset_email_html)
    email = EmailMultiAlternatives(
        subject=f'¡Nos pasa a tod@s!',
        body=password_reset_email_content,
        from_email=default_from_email,
        to=[user.email]
    )

    email.attach_alternative(password_reset_email_html,"text/html")
    print(f'enviando mail a {user.email}')
    email.send(fail_silently=False)
    


    
