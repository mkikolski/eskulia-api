from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from .models import Medicine
from .serializers import MedicineSerializer

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
