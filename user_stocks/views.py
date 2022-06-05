# from .models import User,Portfolio,Stocks
from .serializers import UserSerializer,LoginSerializer,PortfolioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

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
# class portfolioAPIView(generics.GenericAPIView):
#   permission_classes=[IsAuthenticated,]
#   serializer_class = PortfolioSerializer

# @api_view(['GET'])
# def portfolio_stocks(request):
    
#     portfolio_info = []
#     stock_list = Stocks.objects.filter(user=request.user)
#     user1 = Portfolio.objects.filter(user=request.user)[0]
#     money = {'spent' : user1.spent, 'earnt' : user1.earnt, 'value' : 0, 'profit': '+'}
#     return money
 









      
    


