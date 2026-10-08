def pedido_analise_to_fhir(pedido):
    return {
        "resourceType": "Observation",
        "id": f"observation-{pedido.id}",
        "status": pedido.status.lower(),
        "subject": {
            "reference": f"Patient/patient-{pedido.paciente.id}"
        },
        "valueString": pedido.resultado or "Sem resultado",
        "note": [{
            "text": pedido.observacoes or ""
        }]
    }
