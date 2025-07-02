from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Stocks)
admin.site.register(UserInfo)
admin.site.register(UserStock)

#admin.site.register(Stock)

@admin.register(Stocks)
class StockAdmin(admin.ModelAdmin) :
    list_display = ('ticker' , 'name' ,  'curr_price')
    search_fields = ('ticker' , 'name')
    #list_filter