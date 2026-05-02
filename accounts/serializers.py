from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and user creation.
    """

    # Write only means this field accepts input but never shows in response
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # Uses Django's built in password rules
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role',
                 'phone', 'company_name', 'skills']
        extra_kwargs = {
            'role': {'required': True}
        }

    def validate(self, attrs):
        """
        validate() runs after individual field validation.
        Here we check if both passwords match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        """
        create() is called when serializer.save() is called in the view.
        We remove password2 since we don't need it anymore.
        """
        validated_data.pop('password2')

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', User.Role.JOB_SEEKER),
            phone=validated_data.get('phone', ''),
            company_name=validated_data.get('company_name', ''),
            skills=validated_data.get('skills', ''),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile.
    Password is excluded — separate endpoint for that.
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'role', 'phone',
            'profile_picture', 'skills', 'resume',
            'company_name', 'company_website', 'company_description'
        ]
        # Email and role cannot be changed after registration
        read_only_fields = ['email', 'role']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    Not a ModelSerializer because we don't directly
    save a model — we handle it manually in the view.
    """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "New passwords do not match."
            })
        return attrs