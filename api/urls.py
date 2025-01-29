from django.urls import path, include
from . import views

urlpatterns = [
    path('notifications/', include('api.notifications.urls')),
]
