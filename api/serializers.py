"""
Moduł serializerów dla API systemu zarządzania lekami.

Zawiera klasy serializerów do konwersji modeli Drug i DrugCode
na format JSON i odwrotnie, umożliwiając komunikację przez API REST.
"""
# serializers.py
from rest_framework import serializers
from .models import Drug, DrugCode

class DrugCodeSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu DrugCode.

    Konwertuje obiekty DrugCode na format JSON i odwrotnie.
    Używany do reprezentacji kodów identyfikacyjnych leków w API.

    Atrybuty:
        model (Model): Model DrugCode używany do serializacji
        fields (list): Lista pól modelu do uwzględnienia w serializacji
    """
    class Meta:
        """
        Metadane serializera DrugCode.

        Określa model i pola, które mają być serializowane.

        Atrybuty:
            model (Model): Powiązany model DrugCode
            fields (list): Lista pól do serializacji: kod_typu i wartość
        """
        model = DrugCode
        fields = ['code_type', 'value']

class DrugSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Drug.

    Konwertuje obiekty Drug na format JSON i odwrotnie, włączając
    w to powiązane kody identyfikacyjne. Używany do reprezentacji
    leków w API.

    Atrybuty:
        codes (DrugCodeSerializer): Zagnieżdżony serializer dla kodów leku
            z opcją many=True dla obsługi wielu kodów i read_only=True
            dla zapobiegania modyfikacji przez API
        model (Model): Model Drug używany do serializacji
        fields (list): Lista pól modelu do uwzględnienia w serializacji
    """
    codes = DrugCodeSerializer(many=True, read_only=True)

    class Meta:
        """
        Metadane serializera Drug.

        Określa model i pola, które mają być serializowane.

        Atrybuty:
            model (Model): Powiązany model Drug
            fields (list): Lista pól do serializacji, zawierająca podstawowe
                informacje o leku oraz powiązane kody
        """
        model = Drug
        fields = ['id', 'name', 'manufacturer', 'active_ingredients', 
                 'dosage_form', 'codes']