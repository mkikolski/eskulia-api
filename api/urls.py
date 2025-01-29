from django.urls import path, include
from . import views

urlpatterns = [
    path('scan/', views.scan_code, name='scan_code'),
    path('notifications/', include('api.notifications.urls')),
]