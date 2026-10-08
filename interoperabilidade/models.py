
from django.db import models

class HL7Resource(models.Model):
    resource_type = models.CharField(max_length=50)  # Patient, Encounter, Observation
    resource_id = models.CharField(max_length=100)
    payload = models.JSONField()  # JSON FHIR completo
    created_at = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.resource_type} - {self.resource_id}"
