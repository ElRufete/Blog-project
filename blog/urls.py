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
    path('blogs/<int:entry_id>/delete_entry', views.delete_entry, name='delete_entry'),
    path('blogs/<int:blog_id>/delete_blog', views.delete_blog, name='delete_blog'),
]