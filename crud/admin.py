from django.contrib import admin

# Register your models here.
from .models import Stocks,UserInfo
admin.site.register(Stocks)
admin.site.register(UserInfo)
