from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .forms import NewUserCreationForm, CustomAuthenticationForm, EditProfileForm, EmailCheckForm
from django.contrib.auth.forms import SetPasswordForm 
from django.shortcuts import get_object_or_404
from emails.tokens import UserActivationToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from emails.views import welcome_email, reset_password_email

from friends.models import FriendsList
from blog.models import Blog

User = get_user_model()

def register(request):
    """Creates the user and sends an activation email to the it's address"""
    if request.method != 'POST':
        form = NewUserCreationForm()
    else:
        form = NewUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            welcome_email(request, new_user)
            messages.info(request, 
                          'Tu cuenta ha sido creada, revisa tu correo para activarla. Recuerda revisar también la carpeta de spam.',
                          extra_tags='accounts')
            return redirect("blog:blogs_list")
        
    context = {'form':form}
    return render(request,'registration/register.html', context)

def login_view(request):
    """Shows a login form"""
    if request.method != 'POST':
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:blogs_list")
        else:
            messages.error(request, _("Nombre de usuario o contraseña no válidos."))
        
    context = {'form':form}
    return render(request,'registration/login.html', context)

def logout_view(request):
    """Logs user out"""
    logout(request)
    return redirect('blog:home')

def user_profile(request, user_id):
    """Shows user profile if it exists"""

    profile_user = get_object_or_404(User, id=user_id)
    profile_friends = FriendsList.objects.get(user=profile_user).friends.all()
    user_friends = []
    if request.user.is_authenticated:
        user_friends = FriendsList.objects.get(user=request.user).friends.all()

    mutuals = set(profile_friends) & set(user_friends)

    profile_user_blogs = Blog.objects.filter(author=profile_user)
    
    context = {'profile_user': profile_user,
               'mutuals' : mutuals,
               'profile_user_blogs' : profile_user_blogs,
            }
    return render(request, 'registration/user_profile.html', context)

@login_required
def edit_profile(request, user_id):
    """Shows a form to update users info"""

    user = User.objects.get(id=user_id)
    if request.method != 'POST':
        form = EditProfileForm(instance=user)
    else:
        form = EditProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect('accounts:user_profile', user.id)
    
    context = {'form': form,
               'user': user}
    return render(request, 'registration/edit_profile.html', context)


def activate_account(request, uid_b64, token):
    """Checks the token and activates the account if token is valid and user exists."""
    try:
        decoded_uid = force_str(urlsafe_base64_decode(uid_b64))
        user = User.objects.get(pk=decoded_uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = UserActivationToken()
    is_valid = token_generator.check_token(user, token)

    if user is not None and not user.is_active and is_valid:
        user.is_active = True
        user.save()
        messages.success(request,'Tu cuenta se ha activado correctamente.', extra_tags='accounts')
        login(request, 
              user,
              backend='django.contrib.auth.backends.ModelBackend'
              )
        return redirect('blog:blogs_list')
    
    messages.error(request, 'Algo ha fallado en la activación de tu cuenta.', extra_tags='accounts')
    return redirect('blog:blogs_list')


def password_reset_request(request):
    """Shows an email input and sends a password reset email to the adress if it's registered"""
    if request.method != 'POST':
        form = EmailCheckForm()
    else:
        form = EmailCheckForm(data=request.POST)
        if form.is_valid():
            email_instance = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email_instance)
                reset_password_email(request, user)
                
            except User.DoesNotExist:
                pass

        messages.info(request, 'En breve recibirás un correo con instrucciones para restablecer tu contraseña.' \
                                'No olvides revisar la carpeta de spam si no recibes ningún correo.')
        return redirect('accounts:login')
    
    context = {'form': form,
               }
    return render(request, 'registration/password_reset_request.html', context)

def reset_password(request, uid_b64, token):
    """Checks the token and renders the reset_password html if it's valid and the user exists"""
    try:
        decoded_uid = force_str(urlsafe_base64_decode(uid_b64))
        user = User.objects.get(pk=decoded_uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    is_valid = token_generator.check_token(user, token)

    if user is not None and is_valid:
        
        if request.method != 'POST':
            form = SetPasswordForm(user)
        else:
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                messages.success(request, 'Contraseña actualizada con éxito. ¡Bienvenid@ de vuelta!', extra_tags='accounts')
                return redirect('blog:blogs_list')

            else:
                messages.error(request, _("Contraseña no válida."))
            
        context = {'form':form,
                   'uid_b64': uid_b64,
                   'token': token}
        return render(request, 'registration/reset_password.html', context)
    
    messages.error(request, 'El enlace de restablecimiento no es válido o ha expirado.')
    return redirect('accounts:login')
