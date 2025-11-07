from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Blog, Entry, EntryComment, CommentResponse
from .forms import BlogForm, EntryForm, EntryCommentForm, CommentResponseForm


def home(request):
    return render(request, 'blog/home.html')


def blogs_list(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render (request, 'blog/blogs_list.html', context)


def entries_list(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    entries = blog.entry_set.order_by('date_added')
    context = {'blog': blog, 'entries': entries}
    return render(request, 'blog/entries_list.html', context)


def entry(request,blog_id,entry_id):
    blog = Blog.objects.get(id=blog_id)
    entry = Entry.objects.get(id=entry_id)
    entries = Entry.objects.all()
    comments = entry.entrycomment_set.order_by('date_added')
    context= {
        'blog': blog,
        'entry': entry,
        'entries': entries,
        'comments': comments,
    }
    return render(request, 'blog/entry.html', context)


@login_required
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data = request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return redirect('blog:blogs_list')
        
    context = {'form': form,}
    return render(request, 'blog/new_blog.html', context)


@login_required
def new_entry(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    check_author(request, blog.author)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.blog = blog
            new_entry.save()
            return redirect('blog:entries_list', blog.id)

    context = {'blog' : blog, 'form': form}
    return render(request, 'blog/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    blog = entry.blog
    check_author(request, blog.author)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:entry', blog.id, entry.id)
        
    context = {'entry':entry, 'blog':blog, 'form':form}
    return render (request, 'blog/edit_entry.html', context)


@login_required
def comment_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    blog = entry.blog
    if request.method != 'POST':
        form = EntryCommentForm()
    else:
        form = EntryCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.entry = entry
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog:entry', blog.id, entry.id)
        
    context = {
        'entry':entry, 
        'blog':blog, 
        'form':form}
    return render (request, 'blog/comment_entry.html', context)


@login_required
def comment_response(request, comment_id):
    comment = EntryComment.objects.get(id=comment_id)
    entry = comment.entry
    blog = entry.blog
    if request.method != 'POST':
        form = CommentResponseForm()
    else:
        form = CommentResponseForm(data=request.POST)
        if form.is_valid():
            new_response = form.save(commit=False)
            new_response.comment = comment
            new_response.author = request.user
            new_response.save()
            return redirect('blog:entry', blog.id, entry.id)
        
    context = {'comment': comment, 
               'entry': entry, 
               'blog': blog, 
               'form': form}
    return render (request, 'blog/comment_response.html', context)


@login_required
def delete_entry(request, entry_id):
    if request.method == 'POST':
        entry = Entry.objects.get(id=entry_id)
        blog = entry.blog
        check_author(request, blog.author)
        entry.delete()
        return redirect('blog:entries_list', blog.id)
    else:
        return redirect('blog:entries_list', blog.id)
    
@login_required
def delete_blog(request, blog_id):
    
    if request.method == 'POST':
        blog = Blog.objects.get(id=blog_id)
        check_author(request, blog.author)
        blog.delete()
        return redirect('blog:blogs_list')
    else:
        return redirect('blog:blogs_list')
    
@login_required
def delete_comment(request, comment_id):

    comment = EntryComment.objects.get(id=comment_id)
    entry = comment.entry
    blog = entry.blog
    if request.method == 'POST':
        check_author(request, comment.author)
        comment.delete()
        return redirect('blog:entry', blog.id, entry.id)
    else:
        return redirect('blog:entry', blog.id, entry.id)
    
@login_required
def delete_response(request, comment_id):
    response = CommentResponse.objects.get(id=comment_id)
    comment = response.comment
    entry = comment.entry
    blog = entry.blog
    if request.method == 'POST':
        check_author(request, response.author)
        response.delete()
        return redirect('blog:entry', blog.id, entry.id)
    else:
        return redirect('blog:entry', blog.id, entry.id)
    

def check_author(request, author):
    if author != request.user:
        raise Http404



