from django.db.models.signals import post_save
from django.dispatch import receiver
from .services.fhir_sender import enviar_bundle_fhir


from usuarios.models import Consulta, Prescricao, PedidoAnalise
from .models import HL7Resource
from .services.fhir_bundle import gerar_bundle_fhir


def atualizar_bundle(consulta):
    paciente = consulta.paciente

    pedidos = PedidoAnalise.objects.filter(consulta=consulta)
    prescricoes = Prescricao.objects.filter(consulta=consulta)

    bundle = gerar_bundle_fhir(
        paciente,
        consulta,
        pedidos,
        prescricoes
    )

    HL7Resource.objects.update_or_create(
        resource_type="Bundle",
        resource_id=f"consulta-{consulta.id}",
        defaults={"payload": bundle}
    )

    # envio seguro
    try:
        sucesso = enviar_bundle_fhir(bundle)

        if sucesso:
            print("FHIR enviado com sucesso")
        else:
            print("Falha no envio FHIR")

    except Exception as e:
        print("Erro FHIR:", e)

@receiver(post_save, sender=Consulta)
def consulta_salva(sender, instance, created, **kwargs):
    if created:
        atualizar_bundle(instance)


@receiver(post_save, sender=Prescricao)
def prescricao_salva(sender, instance, created, **kwargs):
    if created:
        atualizar_bundle(instance.consulta)


@receiver(post_save, sender=PedidoAnalise)
def exame_salvo(sender, instance, created, **kwargs):
    if created:
        atualizar_bundle(instance.consulta)
