from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

from core import settings
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('chatboot.urls')), 
    path('sobre/', views.sobre, name='sobre'),
    path('servico/', views.servicos, name='servicos'),
    path('user/', include('usuarios.urls')),
    path('contacto/', views.contacto, name='contacto'),
    path("api/chat/", views.chat_api, name='chat_gemini_view'),  # pode manter
    path("agendar/", views.agendar, name='agendar'),
    path('remarconsulta/<int:agenda_id>/', views.remarcarage, name='remarconsulta'),
    path('cancelar_consulta/<int:agenda_id>/', views.cancelar_consulta, name='cancelar_consulta'),
    path('api/', include('interoperabilidade.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)