from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']

        if pw != repeated_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        account = User(
            email=self.validated_data['email'], 
            username=self.validated_data['username']
        )
        account.set_password(pw)
        account.save()
        return account

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()