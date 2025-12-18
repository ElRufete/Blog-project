
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [ 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
]

