from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model) :
    user = models.OneToOneField(User ,  on_delete=models.CASCADE)
    panCard =  models.CharField(max_length=100)
    phoneNumber  = models.CharField(max_length=15)
    profile_pic  =  models.ImageField('profile_pic/')
    panCard_Image =  models.ImageField('pancard/')

class Stocks(models.Model):
    ticker   =  models.CharField(max_length=10)
    name =  models.CharField(max_length=300)
    description  =  models.CharField(max_length =5000)
    curr_price =  models.FloatField()

    def __str__(self):
        return  self.name
class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    buyPrice = models.FloatField()
    buyQuantity = models.IntegerField()
    purchaseDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.name} - {self.user}"

    @property
    def total_value(self):
        if self.stock and self.stock.curr_price and self.buyQuantity:
            return self.buyQuantity * self.stock.curr_price
        return 0



# Create your models here.