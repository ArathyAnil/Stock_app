from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Stocks,Portfolio

admin.site.register(User,UserAdmin)
admin.site.register(Stocks)
admin.site.register(Portfolio)

# Register your models here.
