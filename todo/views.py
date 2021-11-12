from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .serializers import userSerializers, LoginSerializer, RegistrationSerializer
from rest_framework import status
from rest_framework import generics
from .serializers import ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from django_rest_passwordreset.models import ResetPasswordToken

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

	email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

	send_mail(

		# title:
		"Password Reset for {title}".format(title="Some website title"),

		# message:
		email_plaintext_message,

		# from:
		"noreply@somehost.local",

		# to:
		[reset_password_token.user.email]
	)
	print(email_plaintext_message)

class userAPIView(APIView):

	def get(self,request):
		users= User.objects.all()
		s1 = userSerializers(users,many=True)
		return Response(s1.data)

class LoginView(APIView):

	def post(self,request):
		s1 = LoginSerializer(data=request.data)
		s1.is_valid(raise_exception=True)
		user = s1.validated_data["user"]
		login(request,user)
		token, created = Token.objects.get_or_create(user=user)
		request.session['user_token']=token.key
		print(request.session['user_token'])
		return Response({"token":token.key,"message":'Login sucessfully.'},status=200)

class LogoutView(APIView):

	authentication_classes = [TokenAuthentication]

	def post(self, request):
		print(request.META.get('HTTP_AUTHORIZATION'))
		logout(request)
		return Response({"message":'Log Out sucessfully.'},status=204)

class RegistrationView(APIView):

	def post(self,request):
		username = self.request.data['username']
		email =  self.request.data['email']
		password = self.request.data['password']
		print(username)

		data={
			"username":username,
			"email":email,
			"password":make_password(password)
		}
		
		s1 = RegistrationSerializer(data=data)
		if s1.is_valid():
			s1.save()
			return Response(s1.data, status=status.HTTP_201_CREATED)
		return Response(s1.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):

	authentication_classes = [TokenAuthentication]

	def put(self,request):
		token = self.request.data['token']
		psw = self.request.data['old_password']
		n_psw = self.request.data['new_password']
		user = Token.objects.filter(key=token).values_list('user_id',flat=True).first()
		u1=User.objects.get(pk=user)
		print(u1)
		print(psw)
		print(request.data)
		if not u1.check_password(psw):
			return Response({"old_password": ["Wrong password."]}, {"message":'Password changed sucessfully.'}, status=status.HTTP_400_BAD_REQUEST)
		
		data={
			"username":u1.username,
			"email":u1.email,
			"password":make_password(n_psw)
		}

		s1 = userSerializers(u1,data=data)

		if s1.is_valid():
			print(u1)
			s1.save()
			print(s1.data)
			return Response(s1.data)
		else:	
			return Response({"error":"error occured"})

class ResetPasswordView(APIView):

	def post(self,request):
		token = self.request.data['token']
		print(self.request.data['password'])
		password=self.request.data['password']
		user = ResetPasswordToken.objects.filter(key=token).values_list('user_id',flat=True).first()
		u1=User.objects.get(pk=user)
		print(token)
		print(u1)
		print(u1.id)

		data={
			"username":u1.username,
			"email":u1.email,
			"password":make_password(password)
		}

		print(data)
		s1 = userSerializers(u1,data=data)
		if s1.is_valid():
			s1.save()
			return Response({"user":user}) 
		else:
			return Response({"error":"error occured"}) 


