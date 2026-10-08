from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from usuarios.models import Medico,Patient,Consulta
from usuarios.models import Consulta,Medico,Patient

from chatboot.utils import create_prompt



def home(request:HttpRequest):
    medicos=Medico.objects.all()
    return render(request,'home.html',{'medicos':medicos})

def sobre(request:HttpRequest):
    medicos=Medico.objects.all()
    return render(request,'sobre.html',{'medicos':medicos})

def servicos(request:HttpRequest):
    return render(request,'servico.html')

def contacto(request:HttpRequest):
    return render(request,'fale.html')


from datetime import datetime

def agendar(request: HttpRequest):

    if request.method == 'POST':

        especialidade = request.POST.get('especialidade')
        medico_id = request.POST.get('medico')

        data_str = request.POST.get('data')
        hora_str = request.POST.get('horario')

        
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        horario = datetime.strptime(hora_str, "%H:%M").time()

        medico = Medico.objects.get(id=medico_id)
        usuario = Patient.objects.get(id=request.session["paciente_id"])

        Consulta.objects.create(
            medico=medico,
            paciente=usuario,
            data=data,           
            horario=horario,    
            tipoConsulta=especialidade
        )

        messages.success(request, 'Consulta agendada com sucesso!')

    medicos = Medico.objects.all()
    return render(request, 'agendar.html', {'medicos': medicos})


def remarcarage(request:HttpRequest,agenda_id:int):
    consulta=Consulta.objects.filter(id=agenda_id).first()
    if request.method=="POST":
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        if data and horario:
            consulta.data=data
            consulta.horario=horario
            consulta.status='PENDENTE'
            consulta.save()
            messages.success(request,'Remarcado com exito')
            return redirect('historico')
        else:
            messages.error(request,'Porfavor preencham os campos')
    
    return render(request,'editaragenda.html',{'consulta':consulta})
            
        
        
def cancelar_consulta(request:HttpRequest,agenda_id:int):
    consulta=Consulta.objects.filter(id=agenda_id).first()
    consulta.status='CANCELADA'
    consulta.save()
    return redirect('historico')
    
    
    
        
    


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        if not prompt:
            return JsonResponse({"response": "Por favor, envie uma pergunta válida."})
        # Recuperar histórico da sessão
        historico = request.session.get("historico_chat", [])

        # Chamada correta
        resposta = create_prompt(prompt, historico)

        # Salvar histórico novamente
        request.session["historico_chat"] = historico


        
        return JsonResponse({"response": resposta})

    return JsonResponse({"error": "Método não permitido"}, status=405)
