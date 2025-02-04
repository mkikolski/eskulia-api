from rest_framework import serializers
from .models import Medicine

class MedicineSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Medicine wykorzystujący Django REST Framework.
    
    Klasa służy do konwersji instancji modelu Medicine do formatu JSON i odwrotnie,
    umożliwiając łatwą serializację i deserializację danych w API.
    
    Attributes:
        model (Medicine): Model, który będzie serializowany.
        fields (str): '__all__' oznacza, że wszystkie pola modelu Medicine będą uwzględnione w serializacji.
    """
    class Meta:
        """
        Klasa Meta definiująca konfigurację serializatora.
        
        Określa model źródłowy oraz pola, które mają być uwzględnione w procesie
        serializacji i deserializacji.
        """
        model = Medicine
        fields = '__all__'
