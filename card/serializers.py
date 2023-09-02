from rest_framework import serializers
from .models import Card, Purchase
from django.db import models

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True, read_only=True)
    expended = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = '__all__'

    def get_expended(self, obj):
        total_expended = obj.purchases.aggregate(total=models.Sum('purchase_cost'))['total']

        return total_expended
