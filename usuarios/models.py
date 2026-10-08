from django.db import models

class Patient(models.Model):
    nome=models.CharField(max_length=100,null=False,blank=False)
    email=models.EmailField(max_length=50,null=False,blank=False)
    dataN=models.DateField()
    telefone=models.IntegerField(null=False,blank=False)
    senha=models.CharField(max_length=100,null=False,blank=False)
    
    
    def __str__(self):
        return f'Patient {self.nome}'
    
    
class Medico(models.Model):
    nome=models.CharField(max_length=100,null=False,blank=False)
    especialidade=models.CharField(max_length=30, choices=[
        ('Cardiologista','Cardiologista'),
        ('Medicina Geral','Medicina Geral'),
        ('Radiologista','Radiologista'),
        ('Pediatria','Pediatria'),
    ])
    n_ordem=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,null=False,blank=False)
    telefone=models.IntegerField(null=False,blank=False)
    status=models.BooleanField(default=True)
    imagem=models.ImageField(upload_to='medico/',blank=True,null=True)
    senha=models.CharField(max_length=100,null=False,blank=False)
    
    
    def __str__(self):
        return self.nome
    
    


class Consulta(models.Model):
    paciente = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    tipoConsulta = models.CharField(
        max_length=30,
        choices=[
            ('Cardiologia', 'Cardiologia'),
            ('Consulta Geral', 'Consulta Geral'),
            ('Radiologia', 'Radiologia'),
            ('Pediatria', 'Pediatria'),
        ]
    )
    status = models.CharField(
        max_length=30,
        default='PENDENTE',
        choices=[
            ('PENDENTE', 'PENDENTE'),
            ('REALIZADA', 'REALIZADA'),
            ('CANCELADA', 'CANCELADA')
        ]
    )

    
    motivo_consulta = models.TextField(blank=True, null=True)
    queixa_principal = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.paciente} - Consulta com {self.medico} em {self.data}'

    
    
class Prescricao(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='prescricoes')
    medicamento_Doze= models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.medicamento} para {self.consulta.paciente}'
    
from django.db import models
from django.contrib.auth import get_user_model

class PedidoAnalise(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('FINALIZADO', 'Finalizado'),
    ]

    paciente = models.ForeignKey('Patient', on_delete=models.CASCADE)
    consulta = models.ForeignKey('Consulta', on_delete=models.CASCADE, related_name='pedidos_analise')
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    
    
    exames = models.JSONField(blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    realizado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f"Pedido #{self.id} - {self.paciente.nome} - {self.status}"
