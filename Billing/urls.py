from django.urls import path
from Billing.views import SingleBillView,CartView,CheckoutView,MyOrdersView,OrderDeleteView,FarmerOrdersView,UpdateOrderStatusView
from Billing.views import AddressView,AddressDetailView,DeleteFarmerOrderView


urlpatterns = [

    path('singlebill/', SingleBillView.as_view()),
    path('singlebill/<int:id>/', SingleBillView.as_view()),
    path("cart/", CartView.as_view()),
    path("cart/<int:pk>/", CartView.as_view()),
    path("address/", AddressView.as_view()),
    path("address/<int:id>/", AddressDetailView.as_view()),
    path("checkout/", CheckoutView.as_view()),
    path("orders/", MyOrdersView.as_view()),
    path("orders/<int:pk>/", OrderDeleteView.as_view()),
    path("farmer-orders/", FarmerOrdersView.as_view()),
    path("farmer-orders/<int:pk>/", UpdateOrderStatusView.as_view()),
    path("farmerorder-delete/<int:pk>/", DeleteFarmerOrderView.as_view()),
    
    


]
