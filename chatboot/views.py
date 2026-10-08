import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chatboot.utils import create_prompt
from chatboot.models import ChatAssistente
from usuarios.models import Patient

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    data = json.loads(request.body)
    prompt = data.get("prompt")

    # Histórico por sessão
    historico = request.session.get("historico_chat", [])

    # Chama a função que gera a resposta
    resposta = create_prompt(prompt, historico)

    # Atualiza a sessão com o histórico
    request.session["historico_chat"] = historico

    # Salva a conversa no banco apenas se paciente_id existir na sessão
    paciente_id = request.session.get("paciente_id")
    if paciente_id:
        try:
            paciente = Patient.objects.get(id=paciente_id)
            ChatAssistente.objects.create(
                paciente=paciente,
                pergunta=prompt,
                resposta=resposta
            )
            print(f"Mensagem salva para paciente_id {paciente_id}")
        except Patient.DoesNotExist:
            print(f"Patient com id {paciente_id} não existe")

    else:
        print("Nenhum paciente logado na sessão")

    return JsonResponse({"response": resposta})
