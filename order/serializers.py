from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer


class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "phone",
            "email",
            "address",
            "address_label",
            "zipcode",
            "items",
            "paid_amount"
        )