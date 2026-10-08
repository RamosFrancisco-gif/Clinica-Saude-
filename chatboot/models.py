from django.db import models
from usuarios.models import Patient

# Create your models here.
class ChatAssistente(models.Model):
    paciente = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="conversas"
    )
    pergunta = models.TextField()
    resposta = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"