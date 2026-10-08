from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from httpcore import request
from .models import Patient, Consulta, Medico, Prescricao
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from chatboot.models import ChatAssistente
from .models import PedidoAnalise
from datetime import datetime


def cadastroPatients(request: HttpRequest):
    if request.method == "POST":
        dataN = request.POST.get("dataN")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        senha = request.POST.get("password")
        if Patient.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado")
            return redirect("cadastroPatients")

        else:
            if not nome and email and telefone and senha:
                messages.error(request, "Campo vazio, preencha-o")
            else:
                if not telefone.isdigit():
                    messages.error(
                        request, "O número de Telefone deve conter apenas Digito"
                    )
                    return redirect("cadastroPatients")
                else:
                    if not "@" in email:
                        messages.error(request, "Digite um email valido")
                        return redirect("cadastroPatients")

                    else:
                        Patient.objects.create(
                            nome=nome,
                            senha=make_password(senha),
                            email=email,
                            dataN=dataN,
                            telefone=telefone,
                        )
                        messages.success(request, "Usuario cadastrado com exito")
                        return redirect("login")
    return render(request, "cadastro.html")


def home_medico(request: HttpRequest):
    medico_id = request.session.get("medico_id")

    if not medico_id:
        return redirect("login")

    agora = datetime.now()
    medico = Medico.objects.get(id=medico_id)

    consultas = Consulta.objects.filter(
        medico=medico_id,
        status="PENDENTE"
    )
    count_pendente = consultas.count()
    count_realizada = Consulta.objects.filter(
        medico=medico_id,
        status="REALIZADA"
    ).count()
    

    search = request.POST.get("search")

    if request.method == "POST" and search:
        consultas = consultas.filter(
            paciente__nome__icontains=search
        )

        if not consultas.exists():
            messages.error(request, "Patient não encontrado")

    return render(
        request,
        "homeMedico.html",
        {
            "medico": medico,
            "paciente_medi": consultas,
            "agora": agora,
            "count_pendente": count_pendente,
            "count_realizada": count_realizada,
        },
    )




def login(request: HttpRequest):

    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")
        paciente = Patient.objects.filter(email=email).first()
        medico = Medico.objects.filter(email=email).first()
        if not paciente:
            if medico:
                if senha == medico.senha:
                    messages.success(request, "Logado com exito")
                    request.session["medico_id"] = medico.id
                    request.session["medico_nome"] = medico.nome.split(" ")[0]
                    request.session["medico_especialidade"] = medico.especialidade
                    request.session.set_expiry(3600)
                    return redirect("homeMedico")
                else:
                    messages.error(request, "Usuario não Encontrado")
                    return redirect("login")

        else:
            if check_password(senha, paciente.senha):
                messages.success(request, "Logado com exito")
                request.session["paciente_id"] = paciente.id
                request.session["paciente_nome"] = paciente.nome.split(" ")[0]
                request.session.set_expiry(3600)
                return redirect("home")
            else:
                messages.error(request, "Senha Incorrecta")

    return render(request, "login.html")


def logout(request: HttpRequest):
    if "paciente_id" in request.session or "medico_id" in request.session:
        request.session.flush()
        return render(request, "home.html")


def perfil(request: HttpRequest):
    paciente_id = request.session["paciente_id"]
    paciente = Patient.objects.filter(id=paciente_id).first()
    return render(request, "perfil.html", {"paciente": paciente})


def historico(request: HttpRequest):
    paciente_id = request.session["paciente_id"]
    paciente = Patient.objects.filter(id=paciente_id).first()
    consultas = Consulta.objects.filter(paciente=paciente)
    return render(request, "historico.html", {"consultas": consultas})


"""def ver_pacientes(request:HttpRequest):
    medico_id = request.session.get('medico_id')
    pacientes=Consulta.objects.filter(medico=medico_id)
    return render(request,)"""


def verifica(request: HttpRequest):
    if request.method == "POST":
        digitos = request.POST.get("digitos")
        if digitos == request.session["codigo"]:
            messages.success(request, "Verificação realizada com sucesso")
            return redirect("resetSenha")
        messages.error(request, "Codigo Desconhecido")
        return redirect("verficar")

    return render(request, "verifica.html")


def esqueceu_Senha(request: HttpRequest):
    if request.method == "POST":
        request.session.flush()
        email = request.POST.get("email")
        paciente = Patient.objects.filter(email=email).first()
        if paciente:
            codigo = get_random_string(length=4, allowed_chars="0123456789")
            request.session["codigo"] = codigo
            request.session["pacienteR_id"] = paciente.id
            request.session.set_expiry(600)
            send_mail(
                "Assunto",
                f"Aqui vem anexado o seu codigo de verificação: {codigo}",
                "ramosfranciscotch@gmail.com",
                [paciente.email],
            )
            messages.success(request, "Codigo de enviado com exito")
            return redirect("verficar")

        else:
            messages.error(request, "Usuario não encontrado")
    return render(request, "esqueSenha.html")


def resetSenha(request: HttpRequest):
    if request.method == "POST":
        senha = request.POST.get("senha")
        Rsenha = request.POST.get("Rsenha")
        if senha == Rsenha:
            paciente = Patient.objects.filter(
                id=request.session["pacienteR_id"]
            ).first()
            paciente.senha = senha
            messages.success(request, "senha alterada com exito")
            return redirect("home")

        else:
            messages.error(request, "As senhas não coicidem")
            return redirect("resetSenha")

    return render(request, "resetSenha.html")


def editeperfil(request: HttpRequest):
    paciente_id = request.session.get("paciente_id")
    if not paciente_id:
        return redirect("login")

    paciente = Patient.objects.filter(id=paciente_id).first()

    if request.method == "POST":
        nome = request.POST.get("nome")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        dataN = request.POST.get("dataN")

        if not check_password(senha, paciente.senha):
            messages.error(request, "Senha errada")
            return render(request, "editarPerfil.html", {"paciente": paciente})

        print(nome)

        if nome:
            paciente.nome = nome
        if telefone:
            paciente.telefone = telefone
        if email:
            paciente.email = email
        if dataN:
            paciente.dataN = dataN

        paciente.save()
        messages.success(request, "Alteração feita com sucesso!")
        print(nome)
        return redirect("perfil")
    return render(request, "editarPerfil.html", {"paciente": paciente})



from chatboot.utils import create_prompt


def gerar_resumo_prontuario(paciente, consultas, conversas):
    historico_texto = ""

    for c in conversas:
        historico_texto += f"""
        Patient: {c.pergunta}
        Assistente: {c.resposta}
        """

    prompt_resumo = f"""
    Gere um resumo clínico estruturado para o seguinte paciente:

    Nome: {paciente.nome}

    Histórico de Conversas:
    {historico_texto}

    Consultas realizadas: {consultas.count()}

    Gere um prontuário médico claro e objetivo.
    """

    resumo = create_prompt(prompt_resumo, [])

    return resumo


def prontuario(request, paciente_id):
    medico_id = request.session.get("medico_id")
    paciente = get_object_or_404(Patient, id=paciente_id)
    medico = Medico.objects.get(id=medico_id)
    if request.method == "POST":
        motivo_consulta = request.POST.get("motivo_consulta")
        queixa_principal = request.POST.get("queixa_principal")
        diagnostico = request.POST.get("diagnostico")

        consulta = Consulta.objects.filter(
            paciente=paciente, medico=medico, status="PENDENTE"
        ).first()
        if consulta:
            consulta.motivo_consulta = motivo_consulta
            consulta.queixa_principal = queixa_principal
            consulta.diagnostico = diagnostico
            consulta.save()

            messages.success(request, "Prontuário atualizado com sucesso!")
            return redirect("examinar", paciente_id=paciente.id)

    consultas = Consulta.objects.filter(paciente=paciente)
    conversas = ChatAssistente.objects.filter(
        paciente=paciente
    ).order_by('criado_em')

    resumo_prontuario = gerar_resumo_prontuario(
        paciente=paciente,
        consultas=consultas,
        conversas=conversas
    )

    return render(
        request,
        'prontuario.html',
        {
            'paciente': paciente,
            'consultas': consultas,
            'conversas': conversas,
            "medico": medico,
            'resumo_prontuario': resumo_prontuario
        }
    )
    
    
def examinar(request, paciente_id):
    paciente = get_object_or_404(Patient, id=paciente_id)
    medico_id = request.session.get("medico_id")
    medico = Medico.objects.get(id=medico_id)
    consulta=Consulta.objects.filter(paciente=paciente, status="PENDENTE").first()


    if request.method == "POST":
        cuidados = request.POST.get("cuidados")
        receita = request.POST.get("receita")
        
        prescricao= Prescricao.objects.create(
            medicamento_Doze=receita,
            observacoes=cuidados,
            consulta=Consulta.objects.filter(paciente=paciente, status="PENDENTE").first()
        )
        Consulta.objects.filter(paciente=paciente, status="PENDENTE").update(
            status="REALIZADA"
        )
        prescricao.save()
        messages.success(request, "Consulta registrada com sucesso!")
        return redirect("homeMedico")

    return render(request, 'examinar.html', {'paciente': paciente,"medico": medico,"consulta":consulta})



def enviar_exames(request:HttpRequest,consulta_id:int):
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("login")
    consulta = get_object_or_404(Consulta, id=consulta_id)
    paciente = consulta.paciente
    medico = get_object_or_404(Medico, id=medico_id)
    if request.method == "POST":
        exames_selecionados = request.POST.getlist("exames[]")
        observacoes = request.POST.get("observacoes", "").strip()
        if not exames_selecionados:
            messages.error(request, "Selecione pelo menos um exame.")
            return redirect("homeMedico")

        pedido_analise=PedidoAnalise(
            paciente=paciente,
            consulta=consulta,
            medico=medico,
            exames=[{"nome": e} for e in exames_selecionados],
            observacoes=observacoes,
            status="PENDENTE"
        )
        pedido_analise.save()
        consulta.status="REALIZADA"
        consulta.save()
        messages.success(request, f"Pedido de exames criado com sucesso (ID: {pedido_analise.id}).")
        return redirect("homeMedico")

    return render(request, "pedidoDeAnalise.html", {
        "paciente": paciente,
        "consulta": consulta,
        "medico": medico
    })
    
    
    
    
def ver_pedidos_analises(request: HttpRequest):
    usuario_id = request.session.get('paciente_id')
    if usuario_id:
        pedidos_analise = PedidoAnalise.objects.filter(
            consulta__in=Consulta.objects.filter(paciente_id=usuario_id)
        )
        return render(request, "verPedidosAnalises.html", {
            "pedidos_analise": pedidos_analise
        })
        
def verReceitas(request: HttpRequest, consulta_id: int):
    paciente_id = request.session.get("paciente_id")
    if not paciente_id:
        return redirect("login")

    consulta = get_object_or_404(Consulta, id=consulta_id, paciente_id=paciente_id)
    prescricao = get_object_or_404(Prescricao, consulta=consulta)

    return render(request, "verRecitas.html", {
        "consulta": consulta,
        "prescricao": prescricao
    })