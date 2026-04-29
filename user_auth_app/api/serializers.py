from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile

# --- NEU: Der Serializer für die Initialen-Anzeige ---
class UserShortSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'fullname']

    def get_fullname(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip() or obj.username
        if " " not in name:
            return f"{name} {name}"
        return name

# --- DEINE BESTEHENDEN SERIALIZER ---
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

class RegistrationSerializer(serializers.ModelSerializer):
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

    def save(self):
        pw = self.validated_data['password']
        fullname = self.validated_data['fullname']
        email = self.validated_data['email']

        name_parts = fullname.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        account = User(
            email=email, 
            username=email, 
            first_name=first_name,
            last_name=last_name
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
    password = serializers.CharField(write_only=True) # Hier habe ich das Passwort-Feld noch ergänzt!