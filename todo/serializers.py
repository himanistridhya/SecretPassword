from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class userSerializers(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields =  '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg = "user is deactive"
                    raise serializers.ValidationError(msg)
            else:
                msg = "Enter correct credentials"
                raise serializers.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise serializers.ValidationError(msg)
        return data

class ChangePasswordSerializer(serializers.Serializer):
	class Meta:
		model = User
		fields = ('old_password', 'new_password') 
