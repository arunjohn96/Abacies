from django.db import models

class ProductsTbl(models.Model):
    product_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Table"
        verbose_name_plural = "Products"


class PurchaseTransactionTbl(models.Model):
    product = models.ForeignKey(
        'ProductsTbl',
        on_delete=models.SET_NULL,
        null=True,
        related_name='purchase_transactions'
    )
    purchase_id = models.CharField(max_length=255, unique=True)
    purchased_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Purchase Transaction Table"
        verbose_name_plural = "Purchase Transactions"
