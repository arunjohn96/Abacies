from rest_framework import serializers
from core import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductsTbl
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product_id')
    class Meta:
        model = models.PurchaseTransactionTbl
        fields = ['id', 'product_id', 'purchase_id', 'purchased_quantity',
        'created_at', 'last_modified']

    def create(self, validated_data):
        try:
            product_id = validated_data.pop('product')['product_id']
            qs = models.ProductsTbl.objects.get(product_id=int(product_id))
            old_purchased_qty = qs.quantity
            purchased_qty = validated_data.get('purchased_quantity')

            qty = old_purchased_qty - purchased_qty
            qs.quantity = qty
            qs.save()
        except (models.ProductsTbl.DoesNotExist, AssertionError):
            raise serializers.ValidationError("Creation Error")

        return models.PurchaseTransactionTbl.objects.create(
        product=qs,**validated_data
        )

class UpdatePurchaseSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product_id', read_only=True)
    class Meta:
        model = models.PurchaseTransactionTbl
        fields = ['id', 'product_id', 'purchase_id', 'purchased_quantity',
        'created_at', 'last_modified']

        read_only_fields = ['id', 'product_id', 'purchase_id', 'created_at',
         'last_modified']

    def update(self, instance, validated_data):
        qs = instance.product
        old_purchased_qty = instance.purchased_quantity
        new_purchased_qty = validated_data.get('purchased_quantity')
        product_qty = qs.quantity

        qty = product_qty - (new_purchased_qty-old_purchased_qty)
        qs.quantity = qty
        qs.save()


        instance.purchased_quantity = new_purchased_qty
        instance.save()
        return instance


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
