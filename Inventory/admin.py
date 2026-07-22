from django.contrib import admin
from .models import Category, Product, FarmerProfile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(FarmerProfile)