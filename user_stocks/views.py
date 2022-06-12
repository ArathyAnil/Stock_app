from ast import Is
from dataclasses import field
import datetime
from tokenize import Name
from urllib import response
from wsgiref import headers
from django.shortcuts import redirect, render
from .models import User,Portfolio,Stocks,Ticker
from .serializers import UserSerializer,LoginSerializer,PortfolioSerializer,StocksSerializer,TickerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import pandas_datareader.data as web
from rest_framework.generics import ListCreateAPIView,ListAPIView
import pandas as pd
import yfinance as yf




class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = ()
  serializer_class = UserSerializer

  def post(self,request):
    serializer = UserSerializer(data=request.data)
    password = request.data['Password']
    confirm_password = request.data['Confirm_Password']
    if password != confirm_password:

      return Response('the entered passwords does not match')

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({
      'data':serializer.data,
        'status': status.HTTP_201_CREATED})


  

class LoginAPIView(RetrieveAPIView):
  serializer_class = LoginSerializer
  
  permission_classes = []
  def post(self, request):
      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      # return Response(status=status.HTTP_200_OK)
      return Response(
          {
              'message': 'Logged in successfully',
              'status': status.HTTP_200_OK,
              'access_token': serializer.data['tokens']['access'],
              'refresh_token': serializer.data['tokens']['refresh'],
              
          })




class TickerAPIView(APIView):
  permission_classes=[IsAuthenticated,]
  serializer_class = TickerSerializer

  def post(self,request):
    serializer = TickerSerializer
    ticker = request.data['ticker']
    start = datetime.date.today()
    # end = datetime.date.today()
    d = yf.download(ticker,start,end=None)
    df = pd.DataFrame(d)
    df.head().to_dict()
    print(df)
    blankIndex=[''] * len(df)
    df.index=blankIndex
    price = df['High']
    # price1 = price.to_json()
    request.session['price']= price 
    request.session['ticker']=ticker


    return Response({
      'message':'Ticker added successfully'
    })



class Buy_StocksAPIView(APIView):
  permission_classes=[IsAuthenticated,]
  serializer_class = PortfolioSerializer

  def post(self,request):
    # serializer = StocksSerializer
    # ticker = request.data['ticker_chose']


    serializer = StocksSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        {
        'message':'Stock Created Successfully',
        'status':status.HTTP_201_CREATED,
        'data':serializer.data,
        
    }
    )


class stocks_boughtAPIView(generics.ListAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = StocksSerializer

  def get_queryset(self):
    return Stocks.objects.filter(name=self.request.user)
    # User = Stocks.objects.filter(name=request.user)
    # serializer = StocksSerializer(User)

class BalnceAPIView(generics.ListAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = StocksSerializer

  def get(self,request):

    user = Stocks.objects.filter(name=request.user)
    current_bal = Portfolio.objects.get(Earnt=5000)
    stock_bought = Stocks.objects.get('Total_price')
    current_bal+=stock_bought
    return Response(
        {
        'message':'Balance Created Successfully',
        'status':status.HTTP_201_CREATED,
        'data':current_bal,
        
    }
    )

class SellAPIView(generics.ListAPIView):

  permission_classes = [IsAuthenticated]
  serializer_class = StocksSerializer

# @api_view(['POST'])
  def post(self,request):
      ticker = request.data['ticker_chose']
      ticker_obj = Stocks.objects.get(ticker_chose= ticker)
      ticker_obj.action = request.data['action']
      if ticker_obj.action == '1':

        ticker_obj.save()
        return Response({'message':'Bought',
                      'status':status.HTTP_200_OK})

      elif ticker_obj.action == '2':
          ticker_obj.delete()
          return Response({'message':'Sold',
                      'status':status.HTTP_200_OK})







  

