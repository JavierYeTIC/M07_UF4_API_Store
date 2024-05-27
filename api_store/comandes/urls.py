from django.urls import path
from . import views

urlpatterns = [
    path("historial/", views.historial, name="historial"),
    path("historialClient/<int:pk>", views.historialClient, name="historialClient"),
    path("historialNoFin/", views.historialNoFin, name="historialNoFin"),
]