from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import EmailVerificationToken, PasswordResetToken, User, UserRole
from apps.authentication.services import generate_email_verification_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_picture',
            'bio',
            'role',
            'is_verified',
            'created_at',
            'updated_at',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'role': {'required': False}}

    def validate_role(self, value):
        if value not in (UserRole.MERCHANT, UserRole.CUSTOMER):
            raise serializers.ValidationError('Role must be merchant or customer.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        generate_email_verification_token(user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        token['is_verified'] = user.is_verified
        return token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        token = RefreshToken(self.validated_data['refresh'])
        token.blacklist()


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            attrs['record'] = EmailVerificationToken.objects.select_related('user').get(token=attrs['token'], is_used=False)
        except EmailVerificationToken.DoesNotExist as exc:
            raise serializers.ValidationError('Invalid verification token.') from exc
        return attrs

    def save(self):
        record = self.validated_data['record']
        record.user.is_verified = True
        record.user.save(update_fields=['is_verified'])
        record.is_used = True
        record.save(update_fields=['is_used'])
        return record.user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            attrs['record'] = PasswordResetToken.objects.select_related('user').get(token=attrs['token'], is_used=False)
        except PasswordResetToken.DoesNotExist as exc:
            raise serializers.ValidationError('Invalid reset token.') from exc
        return attrs

    def save(self):
        record = self.validated_data['record']
        user = record.user
        user.set_password(self.validated_data['password'])
        user.save(update_fields=['password'])
        record.is_used = True
        record.save(update_fields=['is_used'])
        return user
