# interoperabilidade/urls.py
from django.urls import path
from .views import exportar_fhir_consulta

urlpatterns = [
    path('fhir/export/consulta/<int:consulta_id>/', exportar_fhir_consulta),
]
