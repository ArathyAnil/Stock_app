
from django.urls import path
from .views import Buy_StocksAPIView, RegisterUserAPIView,LoginAPIView,stocks_boughtAPIView,BalnceAPIView,TickerAPIView,SellAPIView
from rest_framework import routers
from . import views

app_name = 'user_stocks'

router = routers.DefaultRouter()




urlpatterns = [

    # path('userdetails',UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),

    path('ticker',TickerAPIView.as_view() , name='ticker'),
    # path('price/',ticker_price.as_view(),name='buy')
    path('stocks/',Buy_StocksAPIView.as_view(),name='bought-stocks'),
    path('balance',BalnceAPIView.as_view(),name='balance'),
    path('sell',SellAPIView.as_view(),name = 'sell' )
]