# from typing_extensions import Required
# from typing_extensions import Required
from msilib import change_sequence
# from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
import datetime



class User(AbstractUser):
    username= models.CharField(max_length=255,unique=True)
    Name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    Phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    # Email = models.EmailField(max_length=255,unique=True)
    Email = models.EmailField(max_length=255,unique=True)
    PAN = models.CharField(max_length=10,unique=True)
    Password = models.CharField(max_length=68,blank=True,validators=[validate_password])
    Confirm_Password = models.CharField(max_length=68,blank=True,validators=[validate_password])
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        print(refresh)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    
    
    def save(self, *args , **kwargs):
        
        self.username = str(self.Name[:3]) + str(self.Phone[-3:] + str(self.created_attrs))
        super().save(*args , **kwargs)
    



class Portfolio(models.Model):

    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    earnt = 8000
    spent = 5000


class Stocks(models.Model):

  portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
  ticker = models.CharField(max_length=10)
  shares = models.PositiveIntegerField(default=0)


class Transaction(models.Model):

    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)



#   @staticmethod
#   def sell(user_id, num_shares, cost_per_share):

#     stock_user = Stocks.objects.get(user=user_id)
#     result = Portfolio.objects.filter(user=stock_user)[0]
#     result.shares -= int(num_shares)
#     if result.shares < 0:
#       result.shares = 0
#       stock_user.earnt += float(cost_per_share) * result.shares
#     else:
#       stock_user.earnt += float(cost_per_share) * int(num_shares)
#     stock_user.save()
#     if result.shares == 0:
#       result.delete()
#     else:
#       result.save()


    




