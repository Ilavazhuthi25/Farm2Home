from django.urls import path
from .views import SignUpView,ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('signup/', SignUpView.as_view()),
     path('token/',  TokenObtainPairView.as_view()),
     path('refresh/', TokenRefreshView.as_view()),
     path('profile/', ProfileView.as_view()),
    
]