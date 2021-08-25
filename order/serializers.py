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


# 장바구니 정보를 보여주기 위한 것
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


class OrderItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )


# 실제 주문 정보(db 저장용)
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

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
            "payment_status",
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order