from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import NewUserCreationForm, CustomAuthenticationForm, EditProfileForm
from django.shortcuts import get_object_or_404

from friends.models import FriendsList
from blog.models import Blog

User = get_user_model()

def register(request):
    if request.method != 'POST':
        form = NewUserCreationForm()
    else:
        form = NewUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("blog:blogs_list")
        
    context = {'form':form}
    return render(request,'registration/register.html', context)

def login_view(request):

    if request.method != 'POST':
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:blogs_list")
        else:
            messages.error(request, _("invalid email or password."))
        
    context = {'form':form}
    return render(request,'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('blog:home')

def user_profile(request, user_id):
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
               'user_avatar' : profile_user.avatar_url(size=100)
            }
    return render(request, 'registration/user_profile.html', context)

@login_required
def edit_profile(request, user_id):
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



    
