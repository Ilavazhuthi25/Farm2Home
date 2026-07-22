from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from.serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class SignUpView(APIView):
    def post(self,request):
         
         
          new_user = User (
            username = request.data["username"],
            role = request.data["role"],
            email = request.data['email'],
            phone_number = request.data['phone_number']
        )
          new_user.set_password(request.data["password"])
          new_user.save()
    


          return Response({
            "message":"User Created Successfully",
            "username":new_user.username,
            "role":new_user.role

        })
    
class LoginView(APIView):

    def post(self,request):
        serializer=CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
             return Response(serializer.errors,status=400)   

          


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
            },
            status=status.HTTP_200_OK
        ) 
    

# class DashboardView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         user = request.user

#         if user.role == "farmer":

#             return Response({

#                 "username": user.username,

#                 "role": user.role,

#                 "dashboard": "Farmer Dashboard"

#             })

#         elif user.role == "customer":

#             return Response({

#                 "username": user.username,

#                 "role": user.role,

#                 "dashboard": "Customer Dashboard"

#             })

#         elif user.role == "admin":

#             return Response({

#                 "username": user.username,

#                 "role": user.role,

#                 "dashboard": "Admin Dashboard"

#             })    

        
    