from django.contrib import admin
from core import models
# Register your models here.
class PurchaseTransactionTblAdmin(admin.ModelAdmin):
    ordering = ['purchased_quantity', 'created_at', 'product_id']
    list_display = ['product_id','purchase_id', 'purchased_quantity','created_at']

    def product_id(self, obj):
        return obj.product.product_id

class ProductsTblAdmin(admin.ModelAdmin):
    ordering = ['product_id', 'name', 'quantity']
    list_display = ['product_id','name','quantity','unit_price']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_id','name','quantity','unit_price')
        }),
    )
admin.site.register(models.ProductsTbl, ProductsTblAdmin)
admin.site.register(models.PurchaseTransactionTbl, PurchaseTransactionTblAdmin)
