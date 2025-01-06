# models.py
from django.db import models

class Drug(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    active_ingredients = models.JSONField()  # Format: {"substance": "amount"}
    dosage_form = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.manufacturer})"

    class Meta:
        ordering = ['name']

class DrugCode(models.Model):
    CODE_TYPES = [
        ('BAR', 'Barcode'),
        ('SN', 'Serial Number'),
        ('LOT', 'Lot Number'),
        ('GTIN', 'Global Trade Item Number'),
        ('OTHER', 'Other')
    ]

    drug = models.ForeignKey(Drug, related_name='codes', on_delete=models.CASCADE)
    code_type = models.CharField(max_length=5, choices=CODE_TYPES)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['code_type', 'value']

    def __str__(self):
        return f"{self.code_type}: {self.value}"