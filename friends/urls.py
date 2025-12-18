from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('new_friend_request/<int:target_id>/', views.new_friend_request, name='new_friend_request'),
    path('friends/friends_page/', views.friends_page, name='friends_page'),
    path('friends/accept_request/<int:fr_request_id>', views.accept_request, name='accept_request'),
    path('friends/decline_request/<int:fr_request_id>', views.decline_request, name='decline_request'),
    path('friends/end_friendship/<int:removee_id>', views.end_friendship, name='end_friendship'),
    path('friends/search_friends/', views.search_friends, name='search_friends'),
               ]