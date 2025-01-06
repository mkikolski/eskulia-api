# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_code, name='scan_code'),
]