from django.db import models
from Authentication.models import User
from Inventory.models import Product


class SingleBill (models.Model):

    bill_number = models.IntegerField(default = 0)
    bill_date = models.DateField( auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    gst = models.FloatField(default=1)
    total_amount = models.FloatField(default=0)





class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"  


class Address(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=10)

    door_no = models.CharField(max_length=20)

    street = models.CharField(max_length=200)

    area = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=6)

    landmark = models.CharField(
        max_length=100,
        blank=True
    )

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"  





class Order(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order_date = models.DateTimeField(auto_now_add=True)

    total_amount = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    address = models.ForeignKey(
    Address,
    on_delete=models.SET_NULL,
    null=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.FloatField(default=0)

    gst = models.FloatField(default=0)

    subtotal = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"


