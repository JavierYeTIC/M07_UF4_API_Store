from django.urls import path
from . import views

urlpatterns = [
    path("nouProducte/", views.nouProducte, name="nouProducte"),
    path("editaProducte/<int:pk>", views.editaProducte, name="editaProducte"),
    path("editaStockProducte/", views.editaStockProducte, name="editaStockProducte"),
    path("eliminaProducte/<int:pk>", views.eliminaProducte, name="eliminaProducte"),
    path("productes/", views.productes, name="productes"),
    path("producte/<int:pk>", views.producte, name="producte"),
]