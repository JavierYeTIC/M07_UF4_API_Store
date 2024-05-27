from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializer import PagamentSerializer
from .models import Payment
from cart.models import Cart
from comandes.models import Order


# Pagar una comanda
@api_view(["POST"])
def pagar(request, id):
    # Comprovar que la ordre existeixi
    try:
        ordre = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response(
            {"Error": "Aquesta ordre no existeix"}, status=status.HTTP_404_NOT_FOUND
        )

    # Demanar les dades de la tarjeta de crèdit
    numero_tarjeta = request.data.get("numero_tarjeta")
    data_caducitat = request.data.get("data_caducitat")
    ccv = request.data.get("ccv")

    # Si no es proporcionen, tornar un error
    if not numero_tarjeta or not data_caducitat or not ccv:
        return Response(
            {"Error": "Falten dades de la targeta"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Canviar el valor de pagat del carretó a true
    carreto = Cart.objects.get(id=ordre.carreto_id)
    carreto.pagat = True
    carreto.save()

    # Recuperar els valors
    ordre = Order.objects.get(carreto=carreto)
    pagament = Payment(ordre=ordre, pagat=True)
    pagament.save()

    pagament_serializer = PagamentSerializer(pagament)
    return Response(pagament_serializer.data, status=status.HTTP_200_OK)


# Consultar estat comanda (esta pagat o no)
@api_view(["GET"])
def estatComanda(request, id):
    try:
        ordre = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response(
            {"Error": "Aquesta ordre no existeix"}, status=status.HTTP_404_NOT_FOUND
        )

    carreto = Cart.objects.get(id=ordre.carreto_id)
    if carreto.pagat == True:
        return Response({"Aquesta comanda està pagada"}, status=status.HTTP_200_OK)
    else:
        return Response({"La comanda no està pagada"}, status=status.HTTP_200_OK)