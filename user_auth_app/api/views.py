from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer


def get_safe_fullname(user_obj):
    """Gibt immer einen Fullname mit zwei Wörtern zurück (für JS-Initialen)."""
    name = f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username
    return name if ' ' in name else f"{name} {name}"


def build_auth_response(user, status_code):
    """Erstellt die Standard-Auth-Antwort mit Token und User-Infos."""
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'fullname': get_safe_fullname(user),
        'email': user.email,
        'user_id': user.pk,
        'message': 'User created successfully.'
    }, status=status_code)


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
            account = serializer.save()
            return build_auth_response(account, 201)
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
            return build_auth_response(user, 200)
        return Response({'error': 'Falsches Passwort.'}, status=400)