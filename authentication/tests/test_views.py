from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class TokenObtainPairViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('authentication:token_obtain_pair')

        User = get_user_model()
        self.user_data = {
            'email': 'hello@test.com',
            'password': 'l4br00t16*'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client = APIClient()
        self.user.is_active = True
        self.user.save()
        
    def test_post_valid_user(self):
        payload = self.user_data
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)