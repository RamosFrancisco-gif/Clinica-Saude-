from django.urls import path 
from .import views

urlpatterns=[
    path('cadastro/',views.cadastroPatients,name='cadastroPatients'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('perfil/',views.perfil,name='perfil'),
    path('historico/',views.historico,name='historico'),
    path('esqueceu_Senha/',views.esqueceu_Senha,name='esqueceu_Senha'),
    path('editeperfil/',views.editeperfil,name='editeperfil'),
    path('resetSenha/',views.resetSenha,name='resetSenha'),
    path('homeMedico/',views.home_medico,name='homeMedico'),
    path('verficar/',views.verifica,name='verficar'),
    path('prontuario/<int:paciente_id>/', views.prontuario, name='prontuario'),
    path('examinar/<int:paciente_id>/', views.examinar, name='examinar'),
    path('pedido_de_analise/<int:consulta_id>/', views.enviar_exames, name='pedido_de_analise'),
    path('ver_pedidos_analises/', views.ver_pedidos_analises, name='ver_pedidos_analises'),
    path('ver_receitas/<int:consulta_id>/', views.verReceitas, name='ver_receitas'),
 

    
]