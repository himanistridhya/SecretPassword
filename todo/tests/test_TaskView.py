from django.http import response
from django.test import TestCase
from Task.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient

class test_addtask(APITestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(username="test", password="python123", email="test@gmail.com")
		self.user.save()

	def test_TaskView_get(self):
		data = {
			'username' : 'test',
			'password' : 'python123'
		}
		u1 = self.client.post(reverse('login'), data=data)

		ApiClient = APIClient()
		ApiClient.credentials(HTTP_AUTHORIZATION='Token'+u1.data['token'])

		response = ApiClient.get('addTask/')

	def test_TaskView_post(self):
		data={
			"username":"test",
			"password":"python123"
		}
		u1 = self.client.post(reverse("login"),data=data)

		session = self.client.session
		session['user_id'] = [u1.data['token']]
		session.save()

		data = {
			"title":'task1',
			"description":"task desc",
			"due_date":'2021-09-19'
		}
		response = self.client.post(reverse('addTask'),data=data)
	
	def test_TaskView_put(self):
		data={
			"username":"test",
			"password":"python123"
		}
		u1 = self.client.post(reverse("login"),data=data)

		

		session = self.client.session
		session['user_id'] = [u1.data['token']]
		session.save()

		data = {
			"title":'task1',
			"description":"task desc",
			"due_date":'2021-09-19'
		}
		response = self.client.post(reverse('addTask'),data=data)

		task = Task.objects.all().first()

		data = {
			"title":'task1',
			"description":"task desc",
			"due_date":'2021-09-19'
		}
		response = self.client.put(reverse('edit', kwargs={'id':task.id}),data=data)

	def test_TaskView_delete(self):
		data={
			"username":"test",
			"password":"python123"
		}
		u1 = self.client.post(reverse("login"),data=data)

		

		session = self.client.session
		session['user_id'] = [u1.data['token']]
		session.save()

		data = {
			"title":'task1',
			"description":"task desc",
			"due_date":'2021-09-19'
		}
		response = self.client.post(reverse('addTask'),data=data)

		task = Task.objects.all().first()

		response = self.client.delete(reverse('edit', kwargs={'id':task.id}),data=data)

