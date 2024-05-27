from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product



# Veure tots els productes
@api_view(["GET"])
def productes(request):
    listaProductes = Product.objects.all()
    listaProductes = listaProductes.filter(estaActiu=True)
    data_serializer = ProductSerializer(listaProductes, many=True)
    return Response({"data": data_serializer.data})


# Veure informació detallada d'un producte
@api_view(["GET"])
def producte(request, pk):
    producte = Product.objects.get(id=pk)
    if producte.estaActiu == False:
        return Response({"Error": "No existe el producto"}, status=400)
    data_serializer = ProductSerializer(producte, many=False)
    return Response({"data": data_serializer.data})


# Afegir nous productes
@api_view(["POST"])
def nouProducte(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# Actualitzar productes
@api_view(["PUT"])
def editaProducte(request, pk):
    try:
        producte = Product.objects.get(id=pk)
        if producte.estaActiu == False:
            return Response({"Error": "No existe el producto"}, status=400)
    except Product.DoesNotExist:
        return Response(status=404)
    serializer = ProductSerializer(producte, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# Actualitzar stock productes
@api_view(["PUT"])
def editaStockProducte(request, pk):
    try:
        producte = Product.objects.get(id=pk)
        if producte.estaActiu == False:
            return Response({"Error": "No existe el producto"}, status=400)
    except Product.DoesNotExist:
        return Response(status=404)
    # Obtener la instancia de las unidades del producto
    unitats_instance = producte.unitats

    # Serializar y actualizar solo las unidades
    serializer = ProductSerializer(producte, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# Eliminar productes a través d'un borrat lògic
@api_view(["DELETE"])
def eliminaProducte(request, pk):
    try:
        producte = Product.objects.get(id=pk)
        if producte.estaActiu == False:
            return Response({"Error": "No existe el producto"}, status=400)
    except Product.DoesNotExist:
        return Response(status=404)
    serializer = ProductSerializer(producte, data=request.data, partial=True)
    if serializer.is_valid():
        producte.estaActiu = False
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)