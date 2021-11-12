from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

class test_LoginView(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(username="abc", password="python123", email="abc@gmail.com")
		self.user.save()

	def test_LogoutView(self):
		data = {
			'username':'abc',
			'password':'python123'
		}
		u1 = self.client.post(reverse('login'),data=data)
		self.assertEqual(u1.status_code, 200)
	
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + u1.data['token'])
		t1 = client.post(reverse('logout'))
		print(t1)

