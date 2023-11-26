from django.contrib.sites import requests
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import RegistrationForm, OrderForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, login
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from django.conf import settings
from telegram import Bot
from telegram import Update
from django.http import JsonResponse


def index(request):
    context = {}

    if request.user.is_authenticated:
        context['user'] = request.user

    return render(request, 'index.html', context)

def rezid(request):

    return render(request, 'rezid.html')
def inf(request):

    return render(request, 'inf.html')
def about(request):

    return render(request, 'about.html')

def home_view(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Замените 'home' на имя вашего URL-маршрута для главной страницы
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth import login, authenticate


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')  # Измените 'home' на имя вашего URL-маршрута для главной страницы
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


# декоратор для запрета входа на страницу по адресу если ты не авторезирова
@login_required
def uslug(request):
    service_types = ServiceType.objects.all()
    return render(request, 'uslug.html', {'service_types': service_types})


@login_required
def service_by_type(request, service_type_id):
    service_type = get_object_or_404(ServiceType, id=service_type_id)
    services = Service.objects.filter(service_type=service_type)
    return render(request, 'service_by_type.html', {'service_type': service_type, 'services': services})


@login_required
def add_to_cart(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Проверка наличия товара в корзине
            existing_order = Order.objects.filter(user=request.user, service=service).first()

            if existing_order:
                existing_order.quantity += quantity
                existing_order.total_cost += existing_order.service.cost * quantity
                existing_order.save()
            else:
                total_cost = service.cost * quantity
                order = Order(user=request.user, service=service, quantity=quantity, total_cost=total_cost)
                order.save()

            messages.success(request, 'Услуга успешно добавлена в корзину!')

            return redirect('service_by_type', service.service_type.id)
    else:
        form = OrderForm()

    context = {'service': service, 'form': form}
    return render(request, 'add_to_cart.html', context)


@login_required
def view_cart(request):
    orders = Order.objects.filter(user=request.user, is_processed=False)

    # Вычисляем общую стоимость в представлении
    total_cost = orders.aggregate(total_cost=Sum('total_cost'))['total_cost']

    return render(request, 'cart.html', {'user_orders': orders, 'total_cost': total_cost})

def total(request):
    # Ваши текущие операции
    orders = Order.objects.filter(user=request.user)

    total_cost = sum(order.total_cost for order in orders)

    return render(request, 'cart.html', {'orders': orders, 'total_cost': total_cost})
def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('view_cart')


# def clear_cart(request):
#     try:
#         # Очистка корзины (удаление всех заказов текущего пользователя)
#         Order.objects.filter(user=request.user).delete()
#
#         # Возвращаем успешный JSON-ответ
#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         # Обработка ошибки и возвращение JSON-ответа с ошибкой
#         return JsonResponse({'status': 'error', 'message': str(e)})
# @csrf_exempt
# def process_order(request):
#     if request.method == 'POST':
#         # Логика обработки заказа...
#
#         # Отмечаем заказы как обработанные
#         user_orders = Order.objects.filter(user=request.user)
#
#         for order in user_orders:
#             order.is_processed = True
#             order.save()
#
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Order
from .telegram_utils import send_telegram_message


@csrf_exempt
@transaction.atomic
def send_telegram_message(chat_id, message_text, total_cost):
    TOKEN = "6148037034:AAGylTPYhWbrZce8J4aCULQF2x7Qns1zv5k"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Добавляем total_cost к тексту сообщения
    message_text += f"\nОбщая стоимость: {total_cost} руб."

    data = {
        'chat_id': chat_id,
        'text': message_text,
    }
    response = requests.post(url, data=data)
    return response.json()


def process_order(request):
    chat_id = "825113753"

    if request.method == 'POST':
        try:
            # Логика обработки заказа...
            user_orders = Order.objects.filter(user=request.user, is_processed=False)

            if user_orders.exists():
                # Выводим информацию о найденных заказах перед их обработкой
                for order in user_orders:
                    print(f"Found unprocessed order: {order}")

                # Собираем информацию о заказах для отправки в Telegram
                message_text = f"Новый заказ от пользователя - {request.user.username}:\n"
                total_cost = 0

                for order in user_orders:
                    message_text += f"{order.service.title} ({order.quantity} шт.) - {order.total_cost} руб.\n"
                    total_cost += order.total_cost

                # Отправка уведомления в Telegram
                send_telegram_message(chat_id, message_text, total_cost)

                # Отмечаем заказы как обработанные
                user_orders.update(is_processed=True)

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No unprocessed orders found'})
        except Exception as e:
            print('Error processing order:', str(e))
            return JsonResponse({'status': 'error', 'message': 'Internal server error'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def clear_cart(request):
    if request.method == 'POST':
        # Логика удаления заказов из корзины
        user_orders = Order.objects.filter(user=request.user)
        user_orders.delete()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
