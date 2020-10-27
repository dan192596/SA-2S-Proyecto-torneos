"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from Juegos.views import JuegoView
from Torneos.views import TorneoView, PartidaView

urlpatterns = [
    path('admin/', admin.site.urls),
    #re_path(r'^juego/(?P<id>\d+)/', JuegoView.as_view(), name='crud_juego'),
    path('partidas/', PartidaView.as_view(), name='crud_partida'),
    path('partidas/<str:id>', PartidaView.as_view(), name='crud_torneo'),
    path('torneo/', TorneoView.as_view(), name='crud_torneo'),
    path('torneo/<int:id>', TorneoView.as_view(), name='crud_torneo'),
    path('juego/', JuegoView.as_view(), name='crud_juego'),
    path('juego/<int:id>', JuegoView.as_view(), name='crud_juego'),
]
