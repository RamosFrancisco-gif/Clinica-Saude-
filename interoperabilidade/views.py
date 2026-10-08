from usuarios.models import Patient,Consulta,Prescricao,PedidoAnalise
from django.http import JsonResponse
from .models import HL7Resource
from .services.fhir_bundle import gerar_bundle_fhir

def exportar_fhir_consulta(request, consulta_id):
    consulta = Consulta.objects.select_related('paciente').get(id=consulta_id)
    pedidos = PedidoAnalise.objects.filter(consulta=consulta)
    prescricoes = Prescricao.objects.filter(consulta=consulta)

    bundle = gerar_bundle_fhir(
        consulta.paciente,
        consulta,
        pedidos,
        prescricoes
    )

    HL7Resource.objects.create(
        resource_type="Bundle",
        resource_id=f"consulta-{consulta.id}",
        payload=bundle
    )

    return JsonResponse(bundle, safe=False)
