from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404


from .models import Blog, Entry, EntryComment, CommentResponse
from .forms import BlogForm, EntryForm, EntryCommentForm, CommentResponseForm

User = get_user_model()

def home(request):
    from django.core.files.storage import default_storage
    print(default_storage.__class__)
    return render(request, 'blog/home.html')


def blogs_list(request):
    blogs = Blog.objects.all()
    fallback = []
    user_blogs = (blogs.filter(author=request.user) 
                if request.user.is_authenticated 
                else Blog.objects.none())
    collaborating_blogs = (blogs.filter(collaborators__collab_list=request.user) 
                        if request.user.is_authenticated else fallback)
    friends_blogs = (blogs.filter(author__friends_list__friends=request.user) 
                     if request.user.is_authenticated else fallback)
    other_blogs = (blogs.exclude(author=request.user)
                   .exclude(collaborators__collab_list=request.user)
                   .exclude(author__friends_list__friends=request.user)
                   if request.user.is_authenticated else blogs)
    
    context = {'blogs': blogs, 
               'user_blogs': user_blogs, 
               'other_blogs':other_blogs,
               'collaborating_blogs': collaborating_blogs,
               'friends_blogs': friends_blogs}
    
    return render (request, 'blog/blogs_list.html', context)


def entries_list(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    entries = blog.entry_set.order_by('date_added')
    blog_collabs = blog.collaborators.collab_list.all()
    collabs_len = len(blog_collabs)
    collabs_word = "Colaboradores" if collabs_len != 1 else "Colaborador"
    collabs_phrase = f'{collabs_len} {collabs_word}'
    context = {'blog': blog, 
               'entries': entries, 
               "blog_collabs": blog_collabs,
               'collabs_phrase': collabs_phrase,}
    
    return render(request, 'blog/entries_list.html', context)


def entry(request,blog_id,entry_id):
    blog = Blog.objects.get(id=blog_id)
    entry = Entry.objects.get(id=entry_id)
    entries = Entry.objects.all()
    entry_comments = entry.entrycomment_set.order_by('-date_added')
    comments = entry_comments.filter(entry=entry)
    comments_len = len(comments)
    comments_word = "Comentarios" if comments_len != 1 else "Comentario"
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
    context= {
        'blog': blog,
        'entry': entry,
        'entries': entries,
        'comments': comments,
        'comments_len': comments_len,
        'comments_word': comments_word,
        'form':form
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
    check_author_or_collab(request, blog.author, blog)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.blog = blog
            new_entry.author = request.user
            new_entry.save()
            return redirect('blog:entries_list', blog.id)

    context = {'blog' : blog, 'form': form}
    return render(request, 'blog/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    blog = entry.blog
    check_author_or_collab(request, blog.author, blog)
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
        check_author_or_collab(request, blog.author, blog)
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
def delete_response(request, response_id):
    response = CommentResponse.objects.get(id=response_id)
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
    """checks if the user is the author of the blog. if not, it raises a 404 error"""
    if author != request.user:
        raise Http404
    
    
def check_author_or_collab(request, author, blog):
    """works like ckeck_author but it also allows blog collaborators"""
    if author == request.user or request.user in blog.collaborators.collab_list.all():
        pass
    else:
        raise Http404




