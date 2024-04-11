from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from dashboard.models import *
from .models import *
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.
class DeliveryInfoAPI(APIView):

    def get(self,request):

        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)

        if int(quarter) == 1:
            qua = [1,2,3]
        elif int(quarter) == 2:
            qua = [4,5,6]
        elif int(quarter) == 3:
            qua = [7,8,9]
        elif int(quarter) == 4:
            qua = [10,11,12]

        order_return_id_list = TransactionInfo.objects.filter(status = 'Refunded').values_list('transactionid',flat=True)
        transaction_qs = Transaction.objects.filter(order_date__year = int(year), order_date__month__in = qua)
        total_delivery = len(transaction_qs)
        shipped = len(transaction_qs.filter(status = "Shipped"))
        in_transit = len(transaction_qs.filter(status = "In transit"))
        delivered = len(transaction_qs.filter(status = "Delivered"))
        return_delivered = len(transaction_qs.filter(transactionid__in = order_return_id_list))

        response = {
            'total_delivery':total_delivery,
            'shipped':shipped,
            'in_transit':in_transit,
            'delivered':delivered,
            'return_delivered':return_delivered,
        }

        return Response(response)
