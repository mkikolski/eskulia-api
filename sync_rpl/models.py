from django.db import models

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
