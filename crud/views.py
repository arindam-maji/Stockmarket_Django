import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import *
from .models import UserStock


@login_required
def index(request):
    user = request.user
    user_stocks = UserStock.objects.select_related('stock').filter(user=user)

    total_invested = 0
    current_value = 0

    for us in user_stocks:
        invested = us.buyPrice * us.buyQuantity
        total_invested += invested
        current_value += us.total_value  # uses @property

    # Prevent divide by zero
    gains = ((current_value - total_invested) / total_invested) * 100 if total_invested else 0

    context = {
        'user_stocks': user_stocks,
        'total_invested': total_invested,
        'current_value': current_value,
        'gains': gains
    }

    return render(request, 'index.html', context)



@login_required
def stocks(request):
    query = request.GET.get('q', '')
    stocks_queryset = Stocks.objects.filter(name__icontains=query) | Stocks.objects.filter(ticker__icontains=query) if query else Stocks.objects.all()

    paginator = Paginator(stocks_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ticker_list = list(page_obj.object_list.values_list('ticker', flat=True))

    context = {
        'page_obj': page_obj,
        'query': query,
        'tickers': ticker_list  # Pass this to template
    }

    return render(request, 'market.html', context)

def logoutView(request) :
    logout(request)
    return redirect('login')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logoutView(request) :
    logout(request)
    return redirect('login')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')


        panCard = request.POST.get('panCard')
        phoneNumber = request.POST.get('phoneNumber')
        profile_pic = request.FILES.get('profile_pic')
        panCard_Image = request.FILES.get('panCard_Image')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')


        user = User(username=username, email=email)
        user.set_password(password)
        user.save()


        user_info = UserInfo(
            user=user,
            panCard=panCard,
            phoneNumber=phoneNumber,
            profile_pic=profile_pic,
            panCard_Image=panCard_Image
        )
        user_info.save()

        login(request, user)
        return redirect('index')

    return render(request, 'register.html')
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["POST"])
def buy(request, id):
    user = request.user
    stock = get_object_or_404(Stocks, id=id)

    try:
        purchase_quantity = int(request.POST.get('quantity'))
        if purchase_quantity <= 0:
            messages.error(request, "Quantity must be positive.")
            return redirect('stocks')

        user_stock, created = UserStock.objects.get_or_create(
            user=user,
            stock=stock,
            defaults={
                'buyQuantity': purchase_quantity,
                'buyPrice': stock.curr_price
            }
        )

        if not created:
            total_quantity = user_stock.buyQuantity + purchase_quantity
            user_stock.buyPrice = (
                (user_stock.buyPrice * user_stock.buyQuantity) +
                (stock.curr_price * purchase_quantity)
            ) / total_quantity
            user_stock.buyQuantity = total_quantity
            user_stock.save()
        #it is slowing down the buy process thats why we will use async
        send_mail(
            subject="Buy Confirmation",
            message=f"You bought {purchase_quantity} shares of {stock.name}.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True
        )

        messages.success(request, f"Successfully bought {purchase_quantity} shares of {stock.name}.")
        return redirect('index')

    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity.")
        return redirect('stocks')

@login_required
def sell(request, id):
    if request.method == 'POST':
        user=request.user
        quantity = int(request.POST.get('quantity', 0))
        stock = get_object_or_404(Stocks, id=id)

        # Check if the user owns the stock
        user_stock = UserStock.objects.filter(user=request.user, stock=stock).first()
        if not user_stock or user_stock.buyQuantity < quantity:
            messages.error(request, f"You don't have enough shares of {stock.name} to sell.")
        else:
            user_stock.buyQuantity -= quantity
            if user_stock.buyQuantity == 0:
                user_stock.delete()
            else:
                user_stock.save()
            send_mail(
            subject="Sell Confirmation",
            message=f"You sold {quantity} shares of {stock.name}.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True)
            messages.success(request, f"📉 You sold {quantity} shares of {stock.name}.")

    return redirect('index')

@login_required
def index(request):
    user = request.user
    user_stocks = UserStock.objects.select_related('stock').filter(user=user)

    total_invested = 0
    current_value = 0

    for us in user_stocks:
        invested = us.buyPrice * us.buyQuantity
        total_invested += invested
        current_value += us.total_value  # uses @property from model

    gains = ((current_value - total_invested) / total_invested) * 100 if total_invested else 0

    context = {
        'user_stocks': user_stocks,
        'total_invested': total_invested,
        'current_value': current_value,
        'gains': gains
    }

    return render(request, 'index.html', context)
