from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    CartSerializer,
    LlistaSerializer,
    ProductSerializer,
)
from catalog.models import Product
from .models import Cart
from comandes.models import Order
from django.shortcuts import get_object_or_404


# Crear carretó
@api_view(["POST"])
def nouCart(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Afegir productes al carretó
@api_view(["POST"])
def afegirProductes(request):
    quantitat = request.data.get("quantitat")
    Cart_id = request.data.get("Cart")
    producte_id = request.data.get("producte")

    # Verificar si el Cart existeix i està actiu
    try:
        Cart = Cart.objects.get(id=Cart_id)
        if not Cart.estaActiu:
            return Response(
                {"Error": "Aquest carretó està tancat, has de crear un de nou"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Cart.DoesNotExist:
        return Response(
            {"Error": "El carretó no existeix"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Crear el producte si el Cart esta actiu
    data = {"quantitat": quantitat, "Cart": Cart_id, "producte": producte_id}

    serializer = LlistaSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar productes del carretó
@api_view(["DELETE"])
def eliminarProducte(request, id):
    producte = get_object_or_404(Product, id=id)

    producte.delete()
    return Response(
        {"message": f"Producte amb id: {id} eliminat"}, status=status.HTTP_200_OK
    )


# Eliminar tot el carretó
@api_view(["DELETE"])
def eliminarCart(request, id):
    Cart = get_object_or_404(Cart, id=id)

    Cart.delete()
    return Response(
        {"message": f"Cart amb id: {id} eliminat"}, status=status.HTTP_200_OK
    )


# Modificar quantitat d'un producte
@api_view(["PUT"])
def modificarQuantitat(request, id):
    try:
        producte = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            {"Error": "El producte no existeix"}, status=status.HTTP_404_NOT_FOUND
        )
    nova_quantitat = request.data.get("quantitat")

    if nova_quantitat is None:
        return Response(
            {"Error": "No s'ha proporcionat cap quantitat"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    producte.quantitat = nova_quantitat
    producte.save()

    serializer = LlistaSerializer(producte)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Consultar el llistat de productes del carretó
@api_view(["GET"])
def llistatProductesCart(request, pk):
    llista = Product.objects.get(Cart_id=pk)
    data_serializer = ProductSerializer(llista, many=True)
    return Response({"data": data_serializer.data})


# Comprar (desactivar el carretó)
@api_view(["DELETE"])
def comprar(request, id):
    try:
        Cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        return Response(
            {"Error": "El carretó no existeix"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = CartSerializer(Cart, data=request.data, partial=True)
    if serializer.is_valid():
        Cart.estaActiu = False
        serializer.save()

        nova_comanda = Order(Cart=Cart)
        nova_comanda.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)