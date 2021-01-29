from rest_framework import viewsets, status, permissions
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import ProductsTbl, PurchaseTransactionTbl
from api_products import serializers
from django.conf import settings
from os import listdir
import csv
import os
import json
from django.core.exceptions import ObjectDoesNotExist


def find_csv_file(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    csv_files = [
        filename for filename in filenames if filename.endswith(suffix)]
    if csv_files:
        csv_files.sort(
            key=lambda x: os.path.getmtime(
                os.path.join(settings.CSV_FILE_PATH, x)), reverse=True)
        print(csv_files)
        return csv_files[0]
    else:
        return None


def csv_to_dictionary(filepath):
    result = []
    with open(filepath, 'r') as data:
        for line in csv.DictReader(data):
            result.append(line)
    return result


def create_new_products(data):
    queryset = ProductsTbl.objects.all().values_list('product_id', flat=True)
    result = []
    qs = set(list(queryset))
    # print(qs)
    for item in data:
        check_key = item.get('Product Id', None)
        # print(check_key)
        if check_key and int(check_key) not in qs:
            try:

                result.append(ProductsTbl(
                    product_id=int(check_key),
                    name=item.get('Product Name', 'NA'),
                    quantity=25000,
                    unit_price=float(item.get('Price Per Quantity', 0)),
                ))
            except (ValueError):
                pass
    if result:
        print(result)
        ProductsTbl.objects.bulk_create(result)

    return


def record_purchase_transactions(data):
    # print("Inside Purchase Record Transaction :::::::::")
    queryset = PurchaseTransactionTbl.objects.all().values_list('purchase_id', flat=True)
    product_qs = ProductsTbl.objects.all()
    result = []
    qs = set(list(queryset))
    # print(qs)
    purchases_dict = {}
    for item in data:
        check_key = item.get('Purchased Id', None)
        if check_key and check_key not in qs:
            try:
                product_id = item.get('Product Id', None)
                product = product_qs.filter(product_id=int(product_id)).first()
                purchase_qty = item.get('Purchased Qty', None)
                if product_id and purchase_qty and product:
                    # print("Here")
                    result.append(PurchaseTransactionTbl(
                        product=product,
                        purchase_id=check_key,
                        purchased_quantity=int(purchase_qty)
                    ))

                    dict_key = purchases_dict.get(str(product_id), None)
                    if dict_key is None:
                        purchases_dict[product_id] = int(purchase_qty)
                    else:
                        purchases_dict[product_id] += int(purchase_qty)

            except (ObjectDoesNotExist):
                pass
    if result:
        # print(result[0])
        PurchaseTransactionTbl.objects.bulk_create(result)
    updated_purchases_list = []
    for key, value in purchases_dict.items():
        product = product_qs.filter(product_id=int(key)).first()
        updated_qty = product.quantity - value
        product.quantity = updated_qty
        updated_purchases_list.append(product)

    if updated_purchases_list:
        print(updated_purchases_list[0])
        ProductsTbl.objects.bulk_update(updated_purchases_list, ['quantity'])

    return


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    This API supports -
    url / _________[GET POST]
    url / {pk} / ____[GET POST PUT DELETE PATCH]

    """
    queryset = ProductsTbl.objects.all().order_by('-created_at')
    serializer_class = serializers.ProductSerializer
    permission_classes = []


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase transactions of products to be viewed
    This API supports -
    url / _____________[GET POST]
    url / {pk} / ______[GET POST PUT DELETE PATCH]
    """
    permission_classes = []
    queryset = PurchaseTransactionTbl.objects.all().order_by('-created_at')
    serializer_class = serializers.PurchaseSerializer

    def update(self, request, pk=None):
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.UpdatePurchaseSerializer(
            obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        qty = instance.purchased_quantity
        qs = instance.product
        qs.quantity += qty
        qs.save()
        instance.delete()


class CreateProductsCsvViewSet(viewsets.ViewSet):
    """
    API endpoint that allows new products to be created from the CSV file
    """
    authentication_classes = []
    permission_classes = []

    def create(self, request, format=None):
        filename = find_csv_file(settings.CSV_FILE_PATH)
        if filename:
            filepath = os.path.join(settings.CSV_FILE_PATH, filename)
            data = csv_to_dictionary(filepath)
            # print(data[:5])
        else:
            return Response(
                {'message': "CSV data not found"}, status.HTTP_404_NOT_FOUND)
        create_new_products(data)
        return Response({'message': 'Action Complete'}, status.HTTP_201_CREATED)


class ProcessPurchaseCsvViewSet(viewsets.ViewSet):
    """
    API endpoint that allows purchase transactions to be created from the CSV file
    """
    authentication_classes = []
    permission_classes = []

    def create(self, request, format=None):
        filename = find_csv_file(settings.CSV_FILE_PATH)
        if filename:
            filepath = os.path.join(settings.CSV_FILE_PATH, filename)
            data = csv_to_dictionary(filepath)
            # print(data[:5])
        else:
            return Response(
                {
                    'message': "CSV data not found"},
                status.HTTP_404_NOT_FOUND
            )
        create_new_products(data)
        record_purchase_transactions(data)
        return Response({'message': 'Action Complete'}, status.HTTP_201_CREATED)


class RefillProductCountViewSet(viewsets.ViewSet):
    """
    API endpoint that allows product refill to be inserted
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.RefillSerializer
    queryset = ProductsTbl.objects.all()

    def create(self, request):
        product_id = request.data.get('product_id', None)
        refill_count = request.data.get('refill_count', None)
        if product_id is None or refill_count is None:
            return Response({'message': 'Check params'}, status.HTTP_400_BAD_REQUEST)

        try:
            obj = self.queryset.get(product_id=int(product_id))
        except ObjectDoesNotExist:
            return Response({'message': 'Not found '}, status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            obj, data={'product_id': product_id, 'refill_count': refill_count})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Refilled successfully',
                'data': serializer.data
            }, status.HTTP_200_OK)

        return Response({
            'message': 'Refill Failed',
            'data': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
