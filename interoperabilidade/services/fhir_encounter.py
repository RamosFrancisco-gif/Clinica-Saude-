from datetime import datetime

def consulta_to_fhir(consulta):
    dt = datetime.combine(consulta.data, consulta.horario)

    return {
        "resourceType": "Encounter",
        "id": f"encounter-{consulta.id}",
        "status": consulta.status.lower(),
        "class": {
            "code": "AMB"
        },
        "subject": {
            "reference": f"Patient/patient-{consulta.paciente.id}"
        },
        "period": {
            "start": dt.isoformat()
        },
        "reasonCode": [{
            "text": consulta.motivo_consulta or consulta.tipoConsulta
        }]
    }
