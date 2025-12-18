from django.urls import path
from . import views

app_name = 'collaborators'
urlpatterns = [
      path('new_collab_request/<int:blog_id>/<int:target_id>', 
            views.new_collab_request, name='new_collab_request'),
      path('remove_collab/<int:blog_id>,<int:target_id>', views.remove_collab,
           name='remove_collab'),
      path('accept_collab_request/<int:request_id>', 
            views.accept_collab_request, name='accept_collab_request'),
      path('decline_collab_request/<int:request_id>', 
            views.decline_collab_request, name='decline_collab_request'),
      path('cancel_collab_request/<int:request_id>', 
            views.cancel_collab_request, name='cancel_collab_request'),
      path('collab_requests_page/', 
            views.collab_requests_page, name='collab_requests_page'),
      path('add_collaborator/<int:blog_id>/', 
            views.add_collab_page, name='add_collab_page'),
      path('remove_collaborator/<int:blog_id>/', 
            views.remove_collab_page, name='remove_collab_page'),
      
]

