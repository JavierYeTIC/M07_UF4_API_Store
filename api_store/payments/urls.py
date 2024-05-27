from django.urls import path
from . import views

urlpatterns = [
    path("pagar/<str:id>", views.pagar, name="pagar"),
    path("estatComanda/<str:id>", views.estatComanda, name="estatComanda"),
]