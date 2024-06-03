from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import *
from django.db.models import Sum, F
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from rest_framework.permissions import IsAuthenticated, AllowAny

class TotalUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        user_qs = UsersInfo.objects.filter(cr_dt__year = int(year), cr_dt__month__in = qua)
        total_user = len(user_qs.values_list('userid'))
        
        response = {
            'total_user':total_user,
        }
        return Response(response)
    

class TotalOrderFulfillAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        total_order_fulfill = len(transaction_qs.values_list('transactionid'))

        response = {
            'total_order_fulfill':total_order_fulfill,
        }
        return Response(response)
    

class TotalRevenueAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        amount = transaction_qs.aggregate(Sum('amount'))
        total_revenue = amount['amount__sum'] or 0

        response = {
            'total_revenue':round(total_revenue,2),
        }
        return Response(response)
    

class TotalGrossProfitAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        transaction_qs = Transaction.objects.filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        amount = transaction_qs.aggregate(Sum('amount'))
        total_revenue = amount['amount__sum'] if amount['amount__sum'] else 0
        # product_info_qs = ProductInfo.objects.filter(productid__in = transaction_qs.values_list('productid',flat=True))
        # cogs = 0

        # Annotate transactions with the cost_making_or_buying from ProductInfo
        annotated_transactions = transaction_qs.annotate(cogs_amount=F('productid__productinfo__amount'))
        cogs = annotated_transactions.aggregate(total_cogs=Sum(F('cogs_amount') * F('qty')))['total_cogs'] if annotated_transactions.aggregate(total_cogs=Sum(F('cogs_amount') * F('qty')))['total_cogs'] else 0

        # for i in product_info_qs:
        #     productid = i.productid
        #     print(productid)
        #     cogs_per_product = i.amount
        #     qty = transaction_qs.filter(productid = productid).aggregate(Sum('qty'))
        #     total_qty_per_product = qty['qty__sum']
        #     cogs += cogs_per_product*total_qty_per_product
        
        # print(cogs,cogss)
        gross_profit = total_revenue - cogs

        response = {
            'total_gross_profit':round(gross_profit,2) 
            }
        return Response(response)


class LastSixMonthsRevenueAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)
        quarter_start_date = datetime(int(year), (int(quarter) - 1) * 3 + 1, 1)
        quarter_end_date = quarter_start_date + relativedelta(months=3, days=-1)
        previous_six_months_start_date = quarter_start_date - relativedelta(months=3)

        def iterate_dates(start_date, end_date):
            current_date = start_date
            while current_date <= end_date:
                yield current_date
                current_date += timedelta(days=32)

        print(previous_six_months_start_date, quarter_end_date)
        response = []
        for date in iterate_dates(previous_six_months_start_date, quarter_end_date):

            year = date.year
            month = date.month
            month_year = date.strftime("%b-%Y")
            order_return_id_list = TransactionInfo.objects.filter(status = 'Refunded').values_list('transactionid',flat=True)
            transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month = month, status = "Delivered")
            amount = transaction_qs.aggregate(Sum('amount'))
            total_revenue = amount['amount__sum'] or 0

            data = {
                'month_year':month_year,
                'total_revenue':round(total_revenue,2),
            }
            response.append(data)
        return Response(response)


class TargetAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)
        quarter_start_date = datetime(int(year), (int(quarter) - 1) * 3 + 1, 1)
        quarter_end_date = quarter_start_date + relativedelta(months=3, days=-1)

        order_return_id_list = TransactionInfo.objects.filter(status = 'Refunded').values_list('transactionid',flat=True)
        transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__lte = quarter_end_date.date(), status = "Delivered")
        amount = transaction_qs.aggregate(Sum('amount'))
        achived = amount['amount__sum'] or 0

        target_in_lanks = 5
        achived_in_lanks = achived/100000

        while True:
            if achived_in_lanks >= target_in_lanks:
                new_target = target_in_lanks + (target_in_lanks * 0.2)
                target_in_lanks = new_target
            else:
                break   

        remaining_in_lanks = target_in_lanks - float(achived_in_lanks)

        response = {
            'target':round(target_in_lanks,2),
            'achived':round(achived_in_lanks,2),
            'remaining':round(remaining_in_lanks,2),
            'percent': round((float(achived_in_lanks)/target_in_lanks)*100, 2)
        }
        return Response(response)