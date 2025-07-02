from django.contrib import admin

from .models import *

# Register other models normally
admin.site.register(UserInfo)
admin.site.register(UserStock)

# Register Stocks with a custom admin class
@admin.register(Stocks)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'curr_price')
    search_fields = ('ticker', 'name')
    # list_filter = [...]
