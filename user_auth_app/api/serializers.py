# 1. Standardbibliothek
# (keine)

# 2. Drittanbieter
from django.contrib.auth.models import User
from rest_framework import serializers

# 3. Lokale Importe
from ..models import UserProfile


class UserShortSerializer(serializers.ModelSerializer):
    """Gibt kompakte User-Infos zurück inkl. zweistelligem Fullname für JS-Initialen."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'fullname']

    def get_fullname(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip() or obj.username
        if ' ' not in name:
            return f"{name} {name}"
        return name


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    """Validiert und erstellt einen neuen User-Account."""

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password', 'fullname']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data.get('password') != data.get('repeated_password'):
            raise serializers.ValidationError({'repeated_password': 'Passwords must match.'})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email address is already in use.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

    def save(self):
        fullname = self.validated_data['fullname'].strip()
        name_parts = fullname.split(' ', 1)
        email = self.validated_data['email']

        account = User(
            email=email,
            username=email,
            first_name=name_parts[0],
            last_name=name_parts[1] if len(name_parts) > 1 else '',
        )
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)