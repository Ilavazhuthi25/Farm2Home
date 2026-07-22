from rest_framework import serializers
from .models import SingleBill,Cart,Order,OrderItem,Address
from Inventory.serializers import ProductSerializer


class SingleBillSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    class Meta:
        model = SingleBill
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_date",
            "total_amount",
            "status",
            "address",
            "items",
        ]





class FarmerOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class FarmerOrderSerializer(serializers.ModelSerializer):

    items = FarmerOrderItemSerializer(many=True, read_only=True)

    customer = serializers.CharField(
        source="user.username",
        read_only=True
    )

    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "order_date",
            "total_amount",
            "status",
            "address",
            "items",
        ]