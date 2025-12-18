from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Blog
from django.contrib.auth import get_user_model
from .models import CollabRequest, CollabList
from notifications.models import CommentNotification, NewEntryNotification
from django.contrib import messages
from django.http import Http404

User = get_user_model()

@login_required
def add_collab_page(request, blog_id):
    user = User.objects.get(id=request.user.id)
    user_friends = user.friends_list.friends.all()
    blog = Blog.objects.get(id=blog_id)
    context = {
        'user': user,
        'user_friends': user_friends,
        'blog': blog,
    }
    check_author(request, blog.author)
    return render(request, 'collaborators/add_collab_page.html', context)

@login_required
def remove_collab_page(request, blog_id):
    user = User.objects.get(id=request.user.id)
    blog = Blog.objects.get(id=blog_id)
    collabs = CollabList.objects.get(blog=blog).collab_list.all()
    context = {
        'user': user,
        'blog': blog,
        'collabs': collabs,
    }
    check_author(request, blog.author)
    return render(request, 'collaborators/remove_collab_page.html', context)


@login_required
def new_collab_request(request, blog_id, target_id):
    request_blog = Blog.objects.get(id=blog_id)
    blog_collaborators_list = CollabList.objects.get(blog=request_blog).collab_list.all()
    request_sender = request.user
    request_receiver = User.objects.get(id=target_id)
    request_sender_friends = request_sender.friends_list.friends.all()
    existing_request = CollabRequest.objects.filter(
        blog=request_blog, sender= request_sender, receiver=request_receiver,
        is_active=True)
    inactive_request = CollabRequest.objects.filter(
        blog=request_blog, sender= request_sender, receiver=request_receiver,
        is_active=False).first()
    next_page = request.POST.get("next")

    if request_sender != request_blog.author:
        messages.error(request, f'solo puedes invitar colaboradores a blogs de los que seas autor', extra_tags="collabs")
        return redirect(next_page or "blog:blogs_list")

    if request_sender == request_receiver:
        messages.error(request, f'No puedes invitarte a colaborar a ti mismo', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)

    if request_receiver not in request_sender_friends:
        messages.info(request, 
            f'{request_receiver} no está en tu lista de amigos. Solo puedes invitar a tus amigos a colaborar', 
            extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    if request_receiver in blog_collaborators_list:
        messages.info(request, f'{request_receiver} ya está en la lista de colaboradores de este blog', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    if existing_request.exists():
        messages.info(request, f'Ya has enviado una solicitud de colaboración a {request_receiver}', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    if inactive_request:
        inactive_request.renew()
        messages.success(request, f'¡Has invitado a {request_receiver} a colaborar en tu blog', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    else:
        CollabRequest.objects.get_or_create(
            blog=request_blog, sender= request_sender, receiver=request_receiver)
        messages.success(request, f'¡Has invitado a {request_receiver} a colaborar en tu blog', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)


@login_required
def remove_collab(request, blog_id,target_id):
    blog = Blog.objects.get(id=blog_id)
    list = CollabList.objects.get(blog=blog)
    collaborators = list.collab_list.all()
    target = User.objects.get(id=target_id)
    next_page = request.POST.get("next")
    check_author(request, blog.author)

    if target not in collaborators:
        messages.error(request, f'{target} no está en la lista de colaboradores del blog',
                       extra_tags='collabs')
        return redirect(next_page or "blog:entries_list", blog.id)
    
    if target not in collaborators:
        messages.error(request, f'{target} no está en la lista de colaboradores del blog',
                       extra_tags='collabs')
        return redirect(next_page or "blog:entries_list", blog.id)
    
    list.remove_collaborator(target)
    messages.success(request, f'Has eliminado a {target} de la lista de colaboradores',
                     extra_tags='collabs')
    return redirect(next_page or "blog:entries_list", blog.id)


@login_required
def accept_collab_request(request, request_id):
    current_request = CollabRequest.objects.get(id=request_id)
    request_blog = current_request.blog
    next_page = request.POST.get('next')
    sender_friends = current_request.sender.friends_list.friends.all()

    if request_blog.author == request.user:
        messages.error(request, '¡No puedes ser colaborador de tu propio blog!', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    if request.user != current_request.receiver:
        messages.error(request, '¡Ups! Parece que esta solicitud no iba dirigida a ti', extra_tags="collabs")
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    if request.user not in sender_friends:
        messages.error(request, f'¡Ups! parece que no estás en la lista de amigos de {current_request.sender}',
                       extra_tags='collabs')
        current_request.cancel()
        return redirect(next_page or "blog:entries_list", request_blog.id)
    
    current_request.accept()
    messages.success(request, f'¡Ahora puedes publicar en el blog "{current_request.blog}"!', extra_tags="collabs")
    return redirect(next_page or "blog:entries_list", request_blog.id)


@login_required
def decline_collab_request(request, request_id):
    current_request = CollabRequest.objects.get(id=request_id)
    request_blog = current_request.blog
    next_page = request.POST.get('next')

    current_request.decline()
    messages.success(request, f'Has rechazado la solicitud de colaboración de {current_request.sender}', extra_tags="collabs")
    return redirect(next_page or "blog:entries_list", request_blog.id)


@login_required
def cancel_collab_request(request, request_id):
    current_request = CollabRequest.objects.get(id=request_id)
    request_blog = current_request.blog
    next_page = request.POST.get('next')

    current_request.cancel()
    messages.success(request, f'Has cancelado la solicitud de colaboración a {current_request.receiver}', extra_tags="collabs")
    return redirect(next_page or "blog:entries_list", request_blog.id)


@login_required
def collab_requests_page(request):
    user = User.objects.get(id=request.user.id)
    user_collab_requests = CollabRequest.objects.filter(receiver=user, is_active=True)
    sent_collab_requests = CollabRequest.objects.filter(sender=user, is_active=True)
    comment_notifications = CommentNotification.objects.filter(target=request.user)
    entry_notifications = NewEntryNotification.objects.filter(target=request.user)
    
    
    context={
        'list_user': user,
        'user_collab_requests' : user_collab_requests,
        'sent_collab_requests' : sent_collab_requests,
        'entry_notifications' : entry_notifications,
        'comment_notifications' : comment_notifications,
    }
    return render(request, 'collaborators/collab_requests.html', context)


def check_author(request, author):
    if author != request.user:
        raise Http404
    