
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [ 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('activate_account/<str:uid_b64>/<str:token>/', views.activate_account, name='activate_account'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('reset_password/<str:uid_b64>/<str:token>/', views.reset_password, name='reset_password'),
]

