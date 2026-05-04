from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer


def get_safe_fullname(user_obj):
    """Return a full name guaranteed to have two words for JS initials rendering."""
    name = f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username
    return name if ' ' in name else f"{name} {name}"


def build_auth_response(user, status_code, message=None):
    """Build the standard authentication response with token and user data."""
    token, _ = Token.objects.get_or_create(user=user)
    
    data = {
        'token': token.key,
        'fullname': get_safe_fullname(user),
        'email': user.email,
        'user_id': user.pk,
    }
    if message:
        data['message'] = message
        
    return Response(data, status=status_code)


class UserProfileList(generics.ListCreateAPIView):
    """List all user profiles or create a new one."""
    
    permission_classes = [IsAuthenticated] 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single user profile."""

    permission_classes = [IsAuthenticated] 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    """Register a new user account and return an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate registration data, create user, and return token."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return build_auth_response(
                account, 
                201, 
                message='User created successfully.'
            )
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    """Authenticate a user by email and password and return an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Look up user by email, verify password, and return token."""
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=400)
        user = authenticate(username=user_obj.username, password=password)
        if user:
            return build_auth_response(user, 200)
        return Response({'error': 'Wrong password.'}, status=400)