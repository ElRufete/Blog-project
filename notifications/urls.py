from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('activity/', views.activity, name='activity'),
]
               