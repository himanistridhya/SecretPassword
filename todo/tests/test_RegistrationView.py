from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

class test_LoginView(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(username="abc", password="python123", email="abc@gmail.com")
		self.user.save()
		self.username = 'xyz'
		self.email = 'xyz@usename.com'
		self.password = 'python123'
	
	def test_RegistrationView(self):
		message = 'Missing fields'
		u1 = self.client.post(reverse('register'), data={'username':self.username, 'email':self.email, 'password':self.password})
		self.assertEqual(u1.status_code, 201, message)

	

