def paciente_to_fhir(paciente):
    return {
        "resourceType": "Patient",
        "id": f"patient-{paciente.id}",
        "name": [{
            "text": paciente.nome
        }],
        "telecom": [
            {
                "system": "phone",
                "value": str(paciente.telefone)
            },
            {
                "system": "email",
                "value": paciente.email
            }
        ],
        "birthDate": paciente.dataN.isoformat() if paciente.dataN else None
    }
