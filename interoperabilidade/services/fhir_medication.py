def prescricao_to_fhir(prescricao):
    return {
        "resourceType": "MedicationRequest",
        "id": f"medication-{prescricao.id}",
        "status": "active",
        "intent": "order",
        "subject": {
            "reference": f"Patient/patient-{prescricao.consulta.paciente.id}"
        },
        "dosageInstruction": [{
            "text": prescricao.medicamento_Doze
        }],
        "note": [{
            "text": prescricao.observacoes or ""
        }]
    }
