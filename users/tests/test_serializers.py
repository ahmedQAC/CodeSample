from django.test import TestCase
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import RegisterUserSerializer

class RegisterUserSerializerTestCase(TestCase):
    def setUp(self):
        # Valid serializer data
        self.serializer_data = {
            'username': 'hello',
            'email': 'hello@test.com',
            'password': 'l4br00t16*',
            'password2': 'l4br00t16*'
        }
        
        self.serializer = RegisterUserSerializer(data=self.serializer_data)
    
    def test_password_validation(self):
        """Test that correct error message is displayed when passwords don't
        match"""
        with self.assertRaisesMessage(serializers.ValidationError, 
                                      "Password fields didn't match."):
            # Update serializer data with different second password
            self.serializer_data['password2'] = 'l4br00t16!'
            invalid_serializer = RegisterUserSerializer(data=self.serializer_data)
            invalid_serializer.is_valid(raise_exception=True)