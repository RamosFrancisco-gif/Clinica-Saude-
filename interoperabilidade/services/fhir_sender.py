import requests
from django.conf import settings


FHIR_SERVER_URL = getattr(
    settings,
    "FHIR_SERVER_URL",
    "http://localhost:8080/fhir"  # servidor local de teste (HAPI FHIR por exemplo)
)


def enviar_bundle_fhir(bundle: dict):
    """
    Envia Bundle FHIR para servidor externo via REST (POST)
    """

    try:
        response = requests.post(
            FHIR_SERVER_URL,
            json=bundle,
            headers={
                "Content-Type": "application/fhir+json"
            },
            timeout=10
        )

        response.raise_for_status()

        return True, response.json()

    except requests.RequestException as e:
        print("Erro ao enviar FHIR:", e)
        return False, str(e)
