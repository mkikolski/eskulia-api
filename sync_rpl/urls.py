from django.urls import path
from .views import MedicineByNameView, MedicineByBarcodeView, FetchMedicines

urlpatterns = [
    path('mbn/<str:name>', MedicineByNameView.as_view(), name='mbn'),
    path('update/', FetchMedicines.as_view(), name='update'),
]