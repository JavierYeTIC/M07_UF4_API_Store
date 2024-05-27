from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import OrdreSerializer
from .models import Order
from core.serializer import ClientSerializer
from core.models import Client
from cart.models import Cart
from cart.serializer import CartSerializer


# Mostrar historial de comandes
@api_view(["GET"])
def historial(request):
    listaComandes = Order.objects.all()
    data_serializer = OrdreSerializer(listaComandes, many=True)
    return Response({"data": data_serializer.data})


# Mostrar historial de comandes per un client concret
@api_view(["GET"])
def historialClient(request, pk):
    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        return Response(status=404)

    # Filtrar los carretones que pertenecen al cliente
    carretons = Cart.objects.filter(client=client)
    # Obtener todas las órdenes relacionadas con los carretones del cliente
    ordres = Order.objects.filter(carreto__in=carretons)
    # Serializar las órdenes
    data_serializer = OrdreSerializer(ordres, many=True)

    return Response({"data": data_serializer.data})


# Mostrar historial de comandes no finalitzades
@api_view(["GET"])
def historialNoFin(request):
    try:
        carretons = Cart.objects.filter(pagat=False)
    except Cart.DoesNotExist:
        return Response(status=404)

    ordres = Order.objects.filter(carreto__in=carretons)
    data_serializer = OrdreSerializer(ordres, many=True)

    return Response({"data": data_serializer.data})