from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    phone_number = models.CharField(max_length=10, unique=True, null=True)


    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("customer", "Customer"),
        ("admin", "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # def __str__(self):
    #     return self.username


# class CustomerProfile(models.Model):

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )

#     address = models.TextField()

#     city = models.CharField(max_length=100)

#     state = models.CharField(max_length=100)

#     pincode = models.CharField(max_length=6)

#     def __str__(self):
#         return self.user.username


# class FarmerProfile(models.Model):

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )

#     farm_name = models.CharField(max_length=200)

#     district = models.CharField(max_length=100)

#     state = models.CharField(max_length=100)

#     farm_size = models.CharField(max_length=50)

#     organic = models.BooleanField(default=False)

#     def __str__(self):
#         return self.farm_name