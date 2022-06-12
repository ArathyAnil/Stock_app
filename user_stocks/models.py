from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
import datetime
from django.utils.dateparse import parse_datetime
import pandas_datareader.data as web
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import yfinance as yf



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
    created_at = models.DateTimeField(null=True,blank=True,default=datetime.datetime.now)


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

        self.created_at = self.created_at.strftime("%Y-%d-%m %H:%M:%S")
        # c1 = created.replace()
        self.username = str(self.Name[:3]) + str(self.Phone[-3:] + str(self.created_at))
        super().save(*args , **kwargs)
    




class Ticker(models.Model):

    ticker = models.CharField(max_length=10)
    
   

    

        


class Stocks(models.Model):
    NONE = 0
    BUY = 1
    SELL = 2
    ACTION_CHOICES = (
        (NONE,('none')),
        (BUY, ('buy')),
        (SELL, ('sell')),
    )
    
    name = models.ForeignKey(User,max_length=255,on_delete=models.CASCADE)
    ticker_chose = models.CharField(max_length=10)
    # total_Price = models.FloatField(default=0, null=True)
    Quantity = models.FloatField(max_length=255)
    Price_per_stock = models.FloatField()
    Total_price = models.FloatField()
    action = models.PositiveIntegerField(choices=ACTION_CHOICES,default=NONE)

    def __str__(self):
        return self.ticker_chose.ticker

    def create(self,*args , **kwargs):
        ticker = self.ticker_chose
        start = datetime.date.today()
        # end = datetime.date.today()
        d = yf.download(ticker,start,end=None)
        df = pd.DataFrame(d)
        blankIndex=[''] * len(df)
        df.index=blankIndex
        self.Price_per_stock=df['High']
        super().save(*args , **kwargs)

    def save(self, *args , **kwargs):

        self.Total_price = self.Quantity * self.Price_per_stock
        super().save(*args , **kwargs)






class Portfolio(models.Model):

    
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks,max_length=10, on_delete=models.CASCADE)
    Earnt = models.FloatField(default=5000)
    Spent = models.FloatField(default=8000)








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


    




