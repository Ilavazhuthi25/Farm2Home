from django.urls import path
from .views import CategoryView,ProductView,FarmerProfileView,CustomerProductView,ProductListView

urlpatterns = [
     path('category/', CategoryView.as_view()),
     path('category/<int:id>/', CategoryView.as_view()),
     path('product/', ProductView.as_view()),
     path('product/<int:id>/', ProductView.as_view()),
     path('farmerprofile/', FarmerProfileView.as_view()),
     path('customerproductview/', CustomerProductView.as_view()),
     path('product-search/', ProductListView.as_view()),

]