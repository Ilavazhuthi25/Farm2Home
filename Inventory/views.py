from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter
from .models import Category, Product,FarmerProfile
from .serializers import CategorySerializer, ProductSerializer, FarmerProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryView(APIView):

    permission_classes = [IsAuthenticated]

  
    def post(self, request):

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response("Category Added Successfully")

        return Response(serializer.errors)


   
    def get(self, request):

        if request.user.is_superuser:
         categories = Category.objects.all()
        else:
         categories = Category.objects.filter(user=request.user)

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


    def patch(self, request, id):

        category = Category.objects.get(
            id=id,
            user=request.user
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response("Category Updated Successfully")

        return Response(serializer.errors)


 
    def delete(self, request, id):

        category = Category.objects.get(
            id=id,
            user=request.user
        )

        category.delete()

        return Response("Category Deleted Successfully")




class ProductView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

   
    def post(self, request):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response("Product Added Successfully")

        return Response(serializer.errors)


    def get(self, request):
        print(request.user)

        if request.user.is_superuser:
            products = Product.objects.all()
        else:
         products = Product.objects.filter(user=request.user)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    
    def patch(self, request, id):

        product = Product.objects.get(
            id=id,
            user=request.user
        )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response("Product Updated Successfully")

        return Response(serializer.errors)


    
    def delete(self, request, id):

        product = Product.objects.get(
            id=id,
            user=request.user
        )

        product.delete()

        return Response("Product Deleted Successfully")
    



class FarmerProfileView(APIView):

    permission_classes = [IsAuthenticated]

    
    def post(self, request):

        serializer = FarmerProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(serializer.errors)


    
    def get(self, request):

        profile = FarmerProfile.objects.get(user=request.user)

        serializer = FarmerProfileSerializer(profile)

        return Response(serializer.data)


    
    def patch(self, request):

        profile = FarmerProfile.objects.get(user=request.user)

        serializer = FarmerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    
    def delete(self, request):

        profile = FarmerProfile.objects.get(user=request.user)

        profile.delete()

        return Response({
            "message": "Farmer Profile Deleted Successfully"
        })    
    

class CustomerProductView(APIView):
    

    def get(self, request):
        
        products = Product.objects.all()

        serializers = ProductSerializer(products, many = True)
        return Response (serializers.data)
    


class ProductListView(ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [SearchFilter]

    search_fields = [
        "product_name",
        "code",
        # "category_name"
    ]        