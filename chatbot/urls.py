from django.urls import path
from .views import MockBotEndpoint

urlpatterns = [
    path('mock/', MockBotEndpoint.as_view(), name='mock'),
]