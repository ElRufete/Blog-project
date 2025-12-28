from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
     path('', views.home, name='home'),
     path('blogs/', views.blogs_list, name='blogs_list'),
     path('blogs/<int:blog_id>/', views.entries_list, name='entries_list'),
     path('blogs/<int:blog_id>/<int:entry_id>/', views.entry, name ='entry'),
     path('new_blog/', views.new_blog, name = 'new_blog'),
     path('blogs/new_entry/<int:blog_id>', views.new_entry, name='new_entry'),
     path('blogs/edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
     path('blog/edit_blog/<int:blog_id>', views.edit_blog, name='edit_blog'),
     path('blogs/<int:entry_id>/delete_entry', views.delete_entry, name='delete_entry'),
     path('blogs/<int:blog_id>/delete_blog', views.delete_blog, name='delete_blog'),
     path('blogs/<int:entry_id>/comment_entry', views.comment_entry, name='comment_entry'),
     path('blogs/<int:comment_id>/comment_response', 
         views.comment_response, name='comment_response'),
     path('blogs/<int:comment_id>/delete_comment', 
         views.delete_comment, name='delete_comment'),
     path('blogs/<int:response_id>/delete_response', 
         views.delete_response, name='delete_response'),
     
]