from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import FriendRequest, FriendsList

User = get_user_model()

def search_friends(request):
    searched = request.GET.get('searched') or request.POST.get('searched')
    if searched:
        users = User.objects.filter(user_name__contains=searched)
        context = {'users': users,'searched' : searched,}
        return render(request, 'friends/search_friends.html', context)
    else:
        return render(request, 'friends/search_friends.html')

    
def new_friend_request(request, target_id):
    target = User.objects.get(id=target_id)
    user_friends = FriendsList.objects.get(user=request.user).friends.all()
    target_friends = FriendsList.objects.get(user=target).friends.all()
    existing_request = FriendRequest.objects.filter(
        sender=request.user, receiver=target, is_active=True)
    reciprocal_request = FriendRequest.objects.filter(
        sender=target, receiver=request.user, is_active=True)
    inactive_request = FriendRequest.objects.filter(
        sender=request.user, receiver=target, is_active=False).first()
    next_page = request.POST.get('next')
    searched = request.POST.get('searched')

    if target == request.user:
        messages.error(request,
             "¡No puedes enviarte una solicitud de amistad a ti mismo!", extra_tags="friends")

    elif existing_request.exists():
        messages.info(request,
             f'Ya has enviado una solicitud de amistad a {target}.', extra_tags="friends")
    
    elif reciprocal_request.exists():
        messages.info(request, 
            f'{target} ya te ha enviado una solicitud. ¡Revísala!', extra_tags="friends")
    
    elif target in user_friends  or request.user in target_friends:
        messages.info(request,
            f'{target} ya está en tu lista de amigos.', extra_tags="friends")
        
    elif inactive_request:
        messages.success(request, 
                "¡Solicitud de amistad enviada!", extra_tags="friends")
        inactive_request.renew()
        
        
    else:
        FriendRequest.objects.create(sender=request.user, receiver=target)
        messages.success(request, 
                "¡Solicitud de amistad enviada!", extra_tags="friends")
    
    return redirect(f"{next_page}?searched={searched}" or 'blog:blogs_list')

def friends_page(request):
    user = User.objects.get(id=request.user.id)
    user_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    user_friends = FriendsList.objects.get(user=request.user).friends.all()

    context={
        'list_user': user,
        'user_friends': user_friends,
        'user_requests' : user_requests,
    }
    return render(request, 'friends/friends_page.html', context)

def accept_request(request, fr_request_id):
    fr_request = FriendRequest.objects.get(id=fr_request_id)
    next_page = request.POST.get('next')
    fr_request.accept()
    if next_page:
        messages.success(request, 
            f'{fr_request.sender} y tú ahora sois amigos.', extra_tags="friends")
        return redirect(next_page)
    else:

        return redirect('blog:blogs_list')
    
def decline_request(request, fr_request_id):
    fr_request = FriendRequest.objects.get(id=fr_request_id)
    target = fr_request.sender
    next_page = request.POST.get('next')
    messages.info(request,
            f'Has rechazado la solicitud de amistad de {target}.', extra_tags="friends")
    fr_request.decline()
    if next_page:
        return redirect(next_page)
    else:
        return redirect('blog:blogs_list')
    
def end_friendship(request, removee_id):
    """
    Looks for the correspondent friend request and makes it inactive.
    Then reciprocally eliminates both users from their friends list.
    """
    removee = User.objects.get(id=removee_id)
    remover = User.objects.get(user_name = request.user)
    friend_request_option_1 = FriendRequest.objects.filter(sender=remover, receiver=removee).first()
    friend_request_option_2 = FriendRequest.objects.filter(sender=removee, receiver=remover).first()
    user_friends_list = FriendsList.objects.get(user = remover)

    if removee not in user_friends_list.friends.all():
        messages.info(request, 
            f'{removee} no está en tu lista de amigos.', extra_tags="friends")
        return redirect(next_page or 'blog:blogs_list')
    
    if friend_request_option_1:
        friend_request_option_1.cancel()

    if friend_request_option_2:
        friend_request_option_2.cancel()

    user_friends_list.unfriend(removee)
    messages.info(request, 
        f'{removee} ha sido eliminado de tu lista de amigos.', extra_tags="friends")
    next_page = request.POST.get('next')
    return redirect(next_page or 'blog:blogs_list')
    
        
    



