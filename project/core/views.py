from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


class Index(View):
    def get(self, request):
        return render(request, 'core/index.html')

@api_view(['GET'])
def filter_1(request):
    """мастера старше 50 лет, заработавшие за ласт день более 700р"""
    #order_date__rt=(datetime.date.today() - datetime.timedelta(days = 1))

    masters = Master.objects.filter(birthday__lt=(datetime.date.today() - datetime.timedelta(days = 365.24*50)))
    orders = Order.objects.filter(order_date__range=[datetime.date.today() - datetime.timedelta(days = 365.24*50), datetime.date.today()], master__in=masters)
    masters_id = {master.id: 0 for master in masters}

    for order in orders:
        masters_id[order.master.id] += float(order.price)

    masters_id = {master: masters_id[master] for master in masters_id if masters_id[master] > 700}
    masters = masters.filter(id__in = [id for id in masters_id])
    serializer = MasterSerializer(masters, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def filter_2(request, thing):
    """мастера до 30 лет, занимающиеся выбранной техникой"""
    masters = Master.objects.filter(repairs_thing=thing)
    serializer = MasterSerializer(masters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_3(request):
    """Мастера, работа которых стоит более 500р"""
    masters = Master.objects.filter(work_price__gt=500)
    serializer = MasterSerializer(masters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_4(request):
    """Мастера, заданного возраста,
     которые занимаются заданной техникой,
    выполнившие заказов на сумму больше,
    чем средняя стоимость заказов мастеров в возрасте старше 45 лет"""
    masters = Master.objects.filter(birthday__year=(datetime.date.today().year - int(request.GET['age'])), repairs_thing=request.GET['thing'])

    mid_masters = Master.objects.filter(birthday__year__lt=(datetime.date.today().year - 45))
    mid_price = 0
    for master in mid_masters:
        mid_price += int(master.work_price)
        print(master.birthday)

    mid_price /= mid_masters.count()

    orders = Order.objects.filter(master__in=masters)

    masters_id = {master.id: 0 for master in masters}

    for order in orders:
        masters_id[order.master.id] += float(order.price)

    masters_id = {master: masters_id[master] for master in masters_id if masters_id[master] > mid_price}
    masters = masters.filter(id__in=[id for id in masters_id])

    serializer = MasterSerializer(masters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_5(request):
    """мастера со стажем от 10 до 20 лет,
    выполнившие заказы на сумму больше,
    чем средняя стоимость заказов,
    выполненных за последние 3 месяца"""

    pass

@api_view(['GET'])
def filter_6(request):
    """Мастера, которые занимаются заданной техникой,
    выполнившие заказов на сумму больше,
    чем средняя стоимость заказов,
    выполненных мастерами со стажем от 2 до 5 лет"""

    pass