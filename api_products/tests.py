from rest_framework.test import APITestCase
from django.shortcuts import reverse
from rest_framework import status
from core.models import ProductsTbl, PurchaseTransactionTbl
# Create your tests here.


class TestProductViews(APITestCase):
    def setUp(self):
        self.product_url = reverse('products-list')
        self.product_data = {
            'product_id': 10215,
            'name': 'Some Product',
            'quantity': 105,
            'unit_price': 100.00
        }

    def test_cannot_create_products(self):
        res = self.client.post(self.product_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product(self):
        res = self.client.post(self.product_url, self.product_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['product_id'],
                         self.product_data['product_id'])
        self.assertEqual(res.data['name'], self.product_data['name'])
        self.assertEqual(res.data['quantity'], self.product_data['quantity'])


class TestPurchaseViews(APITestCase):
    def setUp(self):
        self.purchase_url = reverse('purchases-list')
        self.purchase_data = {
            'product_id': 10215,
            'purchase_id': '8d7qdouiabnsdodAY9DQJp09',
            'purchased_quantity': 90,
        }
        self.product = ProductsTbl.objects.create(
            product_id=10216,
            name='Some Product',
            quantity=100,
            unit_price=100.00
        )
        self.purchase = PurchaseTransactionTbl.objects.create(
            product=self.product,
            purchase_id='d6asd65asd654as5d4',
            purchased_quantity=75
        )
        self.purchase_detail_url = reverse(
            'purchases-detail', kwargs={'pk': self.purchase.pk})

    def test_cannot_create_purchase(self):
        res = self.client.post(self.purchase_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_purchase_wrong_data(self):
        res = self.client.post(self.purchase_url, self.purchase_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_with_data(self):
        product = ProductsTbl.objects.create(
            product_id=10215,
            name='Some Product',
            quantity=105,
            unit_price=100.00
        )
        qty = product.quantity
        res = self.client.post(self.purchase_url, self.purchase_data)
        new_qty = ProductsTbl.objects.get(
            product_id=res.data['product_id']).quantity
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['product_id'],
                         self.purchase_data['product_id'])
        self.assertEqual(res.data['purchase_id'],
                         self.purchase_data['purchase_id'])
        self.assertEqual(res.data['purchased_quantity'],
                         self.purchase_data['purchased_quantity'])
        self.assertEqual(
            new_qty, (qty - self.purchase_data['purchased_quantity']))

    def test_cannot_update_purchase(self):
        res = self.client.put(self.purchase_detail_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_purchase(self):
        data = {'purchased_quantity': 50}

        qty = self.product.quantity
        old_qty = self.purchase.purchased_quantity
        new_qty = data['purchased_quantity']

        qty = qty - (new_qty - old_qty)
        res = self.client.put(self.purchase_detail_url, data)

        check_qty = ProductsTbl.objects.get(id=self.product.pk).quantity
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['purchased_quantity'],
                         data['purchased_quantity'])
        self.assertEqual(qty, check_qty)

    def test_cannot_delete_purchase(self):
        res = self.client.delete(
            reverse('purchases-detail', kwargs={'pk': 100}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_purchase(self):
        qty = self.product.quantity
        purchase_quantity = self.purchase.purchased_quantity

        res = self.client.delete(self.purchase_detail_url)
        new_qty = ProductsTbl.objects.get(id=self.product.id).quantity

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(new_qty, (qty + purchase_quantity))
