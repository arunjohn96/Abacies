from rest_framework import serializers
from core import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductsTbl
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseTransactionTbl
        fields = '__all__'

class ImportCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseTransactionTbl
        fields = '__all__'


class RefillSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    refill_count = serializers.IntegerField(source='quantity')

    def update(self, instance, validated_data):
        count = validated_data.get('quantity', None)
        if count is not None:
            instance.quantity = instance.quantity+count
            instance.save()

        return instance
