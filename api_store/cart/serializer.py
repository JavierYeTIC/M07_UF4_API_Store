from rest_framework import serializers
from .models import Cart
from comandes.models import Order
from catalog.models import Product
from catalog.serializer import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class LlistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Product
        fields = "_all_"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"