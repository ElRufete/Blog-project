from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from www.settings import DEFAULT_FROM_EMAIL

def welcome_email(request):
    context = {'user_name': request.user.user_name}
    welcome_email_html = render_to_string("emails/welcome_email.html",context)
    welcome_email_content = strip_tags(welcome_email_html)
    email = EmailMultiAlternatives(
        subject=f'¡Bienvenid@ a la blogoteca, {request.user.user_name}!',
        body=welcome_email_content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[request.user.email]
    )

    email.attach_alternative(welcome_email_html,"text/html")
    email.send(fail_silently=False)

    return redirect('blog:home')
