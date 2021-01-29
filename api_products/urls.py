from django.urls import path, include
from rest_framework import routers
from api_products import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'purchases', views.PurchaseViewSet, basename='purchases')
router.register(r'import/csv/products', views.CreateProductsCsvViewSet, basename='product-add')
router.register(r'import/csv/purchase_transactions', views.ProcessPurchaseCsvViewSet, basename='csv processing')
router.register(r'refill', views.RefillProductCountViewSet, basename='refill')


urlpatterns = [
    path('', include(router.urls)),
    # path('import/data/', views.ProcessPurchaseCsv),
]
