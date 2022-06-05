
from django.urls import path
from .views import RegisterUserAPIView,LoginAPIView
from rest_framework import routers
from . import views

app_name = 'user_stocks'

router = routers.DefaultRouter()




urlpatterns = [

    # path('userdetails',UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    # path('portfolio/',portfolioAPIView.as_view())

]