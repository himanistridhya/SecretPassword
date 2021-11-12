from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.


class TaskView(APIView):

	def get(self,request):
		# u1=get_user(self.request)
		token = request.META.get('HTTP_AUTHORIZATION')
		print(token)
		user = Token.objects.filter(key=token).values_list('user_id',flat=True).first()
		print(user)
		u1=User.objects.get(pk=user)
		tasks = Task.objects.filter(user=u1.id)
		s1 = TaskSerializer(tasks,many=True)
		return Response(s1.data)

	@csrf_exempt
	def post(self,request):
		user=User.objects.get(pk=(Token.objects.filter(key=request.session['user_token']).values_list('user_id',flat=True).first()))
		data={
			"title":request.data['title'],
			"description":request.data['description'],
			"due_date":request.data['due_date'],
			"user":user.id
		}
		print(data)
		serializer = TaskSerializer(data=data)
		if serializer.is_valid():
			print(data)
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		else:
			return Response({"data":"ERROR"})

	def put(self,request,id):
		print(request.session['user_token'])
		user=User.objects.get(pk=(Token.objects.filter(key=request.session['user_token']).values_list('user_id',flat=True).first()))
		print(user)
		task=Task.objects.get(pk=id)
		if task.user==user:
			data={
				"title":request.data['title'],
				"description":request.data['description'],
				"due_date":request.data['due_date'],
				"user":user.id
			}
			s1 = TaskSerializer(task,data=data)
			if s1.is_valid():
				s1.save()
				return Response(s1.data,status=status.HTTP_201_CREATED)
			else:
				return Response({"msg":"ERROR"})
		else:
			return Response({"msg":"You do not have permission to update this task"})

	def delete(self,request,id):
		user=User.objects.get(pk=(Token.objects.filter(key=request.session['user_token']).values_list('user_id',flat=True).first()))
		task=Task.objects.get(pk=id)

		if task.user==user:
			task.delete()
			return Response({"msg":"Done"})
		else:
			return Response({"msg":"You do not have permission to delete this task"})