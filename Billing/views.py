from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import SingleBill,Cart,Order,OrderItem,Address
from Inventory.models import Product
from .serializers import SingleBillSerializer,CartSerializer,OrderSerializer,FarmerOrderSerializer,ProductSerializer,AddressSerializer


class SingleBillView(APIView):
    def post(self, request):

        product_data = Product.objects.get(id=request.data['product_id'])

        quantity = int(request.data['quantity'])

        amount_without_gst = quantity * product_data.price
        gst_amount = (amount_without_gst * product_data.gst) / 100

        new_bill = SingleBill(
            bill_number=request.data['bill_number'],
            # bill_date=request.data['bill_date'],
            product_id=request.data['product_id'],
            quantity=quantity,
            price=amount_without_gst,
            gst=gst_amount,
            total_amount=amount_without_gst + gst_amount
        )

        new_bill.save()

        return Response("Bill saved")
    
  
    
    def patch (self,request,id):
        print(id)
        print(request.data)
        product_data = Product.objects.get(id = request.data['product_id'])
        amount_without_gst = request.data['quantity'] * product_data.price
        gst_amount = (amount_without_gst * product_data.gst) /100

        the_bill = SingleBill.objects.filter(id = id)
        the_bill.update(
            bill_number = request.data ['bill_number'],
            # bill_date = request.data['bill_date'],
            product_id = request.data['product_id'],
            quantity = request.data['quantity'],
            price = amount_without_gst,
            gst = gst_amount,
            total_amount = amount_without_gst + gst_amount

        )
        return Response("Bill Updated")

    def delete(self,request,id):
        bill = SingleBill.objects.get(id = id )
        bill.delete()
        the_bill = SingleBill.objects.all()
        all_bill = SingleBillSerializer(the_bill,many=True).data
        return Response(all_bill)

        
        return Response("Data deleted")
    

class CartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = Cart.objects.filter(user=request.user)

        serializer = CartSerializer(cart, many=True)

        return Response(serializer.data)


    def post(self, request):

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


    def patch(self, request, pk):

        try:
            cart = Cart.objects.get(id=pk, user=request.user)

        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart.quantity = request.data.get("quantity", cart.quantity)
        cart.save()

        serializer = CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        try:
            cart = Cart.objects.get(id=pk, user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart.delete()

        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )


class AddressView(APIView):

    permission_classes = [IsAuthenticated]

    
    def get(self, request):

        address = Address.objects.filter(user=request.user)

        serializer = AddressSerializer(address, many=True)

        return Response(serializer.data)

   
    def post(self, request):

        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AddressDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, id):

        try:

            return Address.objects.get(
                id=id,
                user=request.user
            )

        except Address.DoesNotExist:

            return None

    
    def patch(self, request, id):

        address = self.get_object(request, id)

        if not address:

            return Response(
                {"error": "Address not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AddressSerializer(
            address,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):

        address = self.get_object(request, id)

        if not address:

            return Response(
                {"error": "Address not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        address.delete()

        return Response(
            {"message": "Address Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response(
                {"message": "Cart is Empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        address_id = request.data.get("address")

        try:
            address = Address.objects.get(
                id=address_id,
                user=request.user
            )
        except Address.DoesNotExist:
            return Response(
                {"message": "Address Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=0
        )

        total = 0

        for item in cart_items:

            subtotal = item.product.price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                gst=item.product.gst,
                subtotal=subtotal
            )

            total += subtotal

        order.total_amount = total
        order.save()

        cart_items.delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )




class MyOrdersView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.filter(user=request.user).order_by("-id")

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)



class OrderDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            order = Order.objects.get(
                id=pk,
                user=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {"message": "Order Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        order.delete()

        return Response(
            {"message": "Order Deleted Successfully"}
        )         
    


class FarmerOrdersView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role == "admin":

            orders = Order.objects.select_related(
                "user",
                "address"
            ).prefetch_related(
                "items__product"
            ).all()

        else:

            orders = Order.objects.select_related(
                "user",
                "address"
            ).prefetch_related(
                "items__product"
            ).filter(
                items__product__user=user
            ).distinct()

        serializer = FarmerOrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data) 
    


class UpdateOrderStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)

        except Order.DoesNotExist:

            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        order.status = request.data.get(
            "status",
            order.status
        )

        order.save()

        serializer = FarmerOrderSerializer(order)

        return Response(serializer.data)
    


class DeleteFarmerOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

       
        if request.user.role != "admin":
            if not order.items.filter(product__user=request.user).exists():
                return Response(
                    {"error": "Permission Denied"},
                    status=status.HTTP_403_FORBIDDEN
                )

        order.delete()

        return Response(
            {"message": "Order Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )