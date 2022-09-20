from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Message




#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username"]


#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
  password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ('username','email', 'password1', 'password2',)
    
    
  def validate(self, attrs):
    if attrs['password1'] != attrs['password2']:
      raise serializers.ValidationError({"password1": "Password2 fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
    )
    user.set_password(validated_data['password1'])
    user.save()
    return user


class MessageSerilaizer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    is_read_receipt = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_is_read_receipt(self, obj):
        return obj.is_read_receipt 

