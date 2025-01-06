# serializers.py
from rest_framework import serializers
from .models import Drug, DrugCode

class DrugCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugCode
        fields = ['code_type', 'value']

class DrugSerializer(serializers.ModelSerializer):
    codes = DrugCodeSerializer(many=True, read_only=True)

    class Meta:
        model = Drug
        fields = ['id', 'name', 'manufacturer', 'active_ingredients', 
                 'dosage_form', 'codes']