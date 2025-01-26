from django.urls import path
from . import views

urlpatterns = [
    path('notifications_handler/', views.notifications_handler, name='notifications_handler'),
]
