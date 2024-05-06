from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
    
    def validate(self, attrs):
        """
        Check that password matches password2.
        """
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    # Override create method to hash password
    # https://stackoverflow.com/questions/56701988/how-to-fix-invalid-password-format-or-unknown-hashing-algorithm-in-a-custom-u
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email']


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username'
        ]