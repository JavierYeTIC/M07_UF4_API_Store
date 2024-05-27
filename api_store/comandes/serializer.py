from rest_framework import serializers
from .models import Order
from core.serializer import ClientSerializer


class OrdreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "_all_"