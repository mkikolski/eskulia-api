from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('send/', 
         views.SendNotificationView.as_view(), 
         name='send-notifications'),
    path('token/update/', 
         views.UpdateFCMTokenView.as_view(), 
         name='update-fcm-token'),
    path('token/delete/', 
         views.DeleteFCMTokenView.as_view(), 
         name='delete-fcm-token'),
]
