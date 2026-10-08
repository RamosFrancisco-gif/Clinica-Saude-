# interoperabilidade/services/fhir_bundle.py
from .fhir_patient import paciente_to_fhir
from .fhir_encounter import consulta_to_fhir
from .fhir_observation import pedido_analise_to_fhir
from .fhir_medication import prescricao_to_fhir

def gerar_bundle_fhir(paciente, consulta, pedidos, prescricoes):
    entries = []

    entries.append({"resource": paciente_to_fhir(paciente)})
    entries.append({"resource": consulta_to_fhir(consulta)})

    for pedido in pedidos:
        entries.append({"resource": pedido_analise_to_fhir(pedido)})

    for prescricao in prescricoes:
        entries.append({"resource": prescricao_to_fhir(prescricao)})

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": entries
    }
