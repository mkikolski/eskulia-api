from django.db import models
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Medicine
from .serializers import MedicineSerializer
from django.db.models import Q
from rest_framework import serializers
from django.urls import path
from .views import MedicineByNameView, MedicineByCodeView

class Medicine(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, null=True, blank=True)
    preparation_type = models.CharField(max_length=100, null=True, blank=True)
    administration_route = models.CharField(max_length=255, null=True, blank=True)
    strength = models.CharField(max_length=100, null=True, blank=True)
    pharmaceutical_form = models.CharField(max_length=255, null=True, blank=True)
    atc_code = models.CharField(max_length=50, null=True, blank=True)
    responsible_entity = models.CharField(max_length=255, null=True, blank=True)
    active_substance = models.TextField(null=True, blank=True)
    packaging = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class MedicineByNameView(APIView):
    def get(self, request, name):
        try:
            medicines = Medicine.objects.annotate(similarity=TrigramSimilarity('name', name)) \
                .filter(similarity__gt=0.3) \
                .order_by('-similarity')

            if not medicines.exists():
                return Response({"error": "Nie znaleziono leku o podanej nazwie."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MedicineSerializer(medicines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class MedicineByCodeView(APIView):
#     def get(self, request, code):
#         try:
#             medicine = Medicine.objects.filter(identifier=code).first()
#             if not medicine:
#                 return Response({"error": "Nie znaleziono leku o podanym identyfikatorze."}, status=status.HTTP_404_NOT_FOUND)
            
#             return Response({"name": medicine.name}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicineByBarcodeView(APIView):
    def get(self, request, barcode):
        try:
            medicine = Medicine.objects.filter(packaging__icontains=barcode).first()

            if not medicine:
                return Response({"error": "Nie znaleziono leku z podanym kodem kreskowym."}, status=status.HTTP_404_NOT_FOUND)

            packaging_details = next(
                (line for line in medicine.packaging.split("\n") if barcode in line), None
            )

            if not packaging_details:
                return Response({"error": "Kod kreskowy nie pasuje do żadnego opakowania."}, status=status.HTTP_404_NOT_FOUND)

            response_data = {
                "name": medicine.name,
                "common_name": medicine.common_name,
                "strength": medicine.strength,
                "pharmaceutical_form": medicine.pharmaceutical_form,
                "packaging_details": packaging_details,
                "active_substance": medicine.active_substance,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



urlpatterns = [
    path('medicine/name/<str:name>/', MedicineByNameView.as_view(), name='medicine-by-name'),
    path('medicine/code/<str:code>/', MedicineByCodeView.as_view(), name='medicine-by-code'),
]
