from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('users:create')
        self.valid_payload = {
            'username': 'hello',
            'email': 'hello@test.com',
            'password': 'l4br00t16*',
            'password2': 'l4br00t16*'
        }
        self.client = APIClient()
    
    def test_valid_post_creates_new_user(self):
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)

        User = get_user_model()
        user = User.objects.get(username=self.valid_payload['username'])
        self.assertEqual(user.username, self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])