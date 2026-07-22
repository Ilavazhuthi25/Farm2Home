from django.db import models
from Authentication.models import User


class Category(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
     return self.category_name




class Product(models.Model):

    user = models.ForeignKey(User, null=True,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.CharField(
    max_length=100,
    default=""
)
 
    product_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    gst = models.IntegerField(default=1)
    stock = models.CharField(max_length=100)
    kg = models.FloatField(default=0) 
    product_image = models.ImageField(
       upload_to = "product/",
       blank = True,
       null = True
       )    


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100, unique=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    profile_image = models.ImageField(
        upload_to="farmers/",
        blank=True,
        null=True
    )
    about = models.TextField(blank=True)
