from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from ..models import UserProfile
from .serializers import (
    UserProfileSerializer, 
    RegistrationSerializer
)

def get_safe_fullname(user_obj):
    name = f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username
    return name if " " in name else f"{name} {name}"

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            save_account = serializer.save()
            token, created = Token.objects.get_or_create(user=save_account)
            
            raw_name = f"{save_account.first_name} {save_account.last_name}".strip()
            name_parts = raw_name.split()
            if len(name_parts) == 1:
                safe_fullname = f"{name_parts[0]} {name_parts[0]}"
            else:
                safe_fullname = raw_name
            
            return Response({
                'token': token.key,
                'fullname': safe_fullname,
                'email': save_account.email,
                'user_id': save_account.pk 
            }, status=201) 
        
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'E-Mail nicht gefunden.'}, status=400)

        user = authenticate(username=user_obj.username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'fullname': get_safe_fullname(user),
                'email': user.email,
                'user_id': user.pk  
            }, status=200)
        else:
            return Response({'error': 'Falsches Passwort.'}, status=400)

# class LogoutView(APIView):
#     def post(self, request):
#         request.auth.delete()
#         return Response(status=200)