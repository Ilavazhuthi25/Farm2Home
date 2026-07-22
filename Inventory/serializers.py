from rest_framework import serializers
from .models import Category, Product,FarmerProfile


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["user"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    farmer = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class FarmerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmerProfile
        fields = "__all__"
        read_only_fields = ["user"]        