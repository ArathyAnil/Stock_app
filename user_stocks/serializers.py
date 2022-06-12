
from dataclasses import fields
from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Stocks, User,Portfolio,Ticker
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):

  class Meta:

    model = User

    fields = ('username', 'Password', 'Confirm_Password','Email','Name','Phone','PAN','id','created_at')
    extra_kwargs = {

      'Password': {'write_only': True},
      'Confirm_Password':{'write_only':True}
      
      
    }
 

    def create(self,validated_data):
        # pass
        instance = self.Meta.model(**validated_data)
        return instance




class LoginSerializer(serializers.ModelSerializer):

    Email = serializers.EmailField(max_length=255, min_length=3,allow_blank=False)
    Password = serializers.CharField(max_length=68,write_only=True)
    tokens = serializers.SerializerMethodField()
    Name = serializers.CharField(max_length=255,allow_blank=False)
  

    def get_tokens(self, obj):

      user = User.objects.get(Q(email=obj['Email']) | Q(Name=obj['Name']))

      return {
          'refresh': user.tokens()['refresh'],
          'access': user.tokens()['access'],
      }


    class Meta:

      model = User

      fields = ['Email','Name','Password','tokens']
        



      def validate(self, attrs):
        user = User.objects.get(Q(Email=attrs['Email']) | Q(Name=attrs['Name']))
        password = attrs.get('Password', '')
        user1 = auth.authenticate(username=user, password=password)

        if not user1:

            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'email': user1.Email,
            'name': user1.Name,
            'tokens': user1.tokens,
        }

class TickerSerializer(serializers.ModelSerializer):


 
  class Meta:

    model = Ticker

    fields = ['ticker']
#     # extra_kwargs = {

#       # 'Price': {'read_only': True},}



class PortfolioSerializer(serializers.ModelSerializer):

  class Meta:

    model = Portfolio

    fields = ['__all__']


class StocksSerializer(serializers.ModelSerializer):

  class Meta:

    model = Stocks

    fields = ['ticker_chose','Quantity','Price_per_stock','name','Total_price','action']

  


    

      



