from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

# Importiere deine eigenen Models und Serializer
from ..models import UserProfile
from .serializers import (
    UserProfileSerializer, 
    RegistrationSerializer
)

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
            
            # Hier passen wir die Antwort auch direkt an dein Frontend an:
            return Response({
                'token': token.key,
                'userId': save_account.pk,
                'email': save_account.email,
                'fullname': f"{save_account.first_name} {save_account.last_name}".strip() or save_account.username
            }, status=201) 
        
        return Response(serializer.errors, status=400) 


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # 1. User anhand der E-Mail suchen
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'E-Mail nicht gefunden.'}, status=400)

        # 2. Mit dem gefundenen Usernamen und Passwort einloggen
        user = authenticate(username=user_obj.username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            
            # Das JSON Paket für dein setAuthCredentials()
            return Response({
                'token': token.key,
                'userId': user.pk,
                'email': user.email,
                'fullname': f"{user.first_name} {user.last_name}".strip() or user.username
            }, status=200)
        else:
            return Response({'error': 'Falsches Passwort.'}, status=400)