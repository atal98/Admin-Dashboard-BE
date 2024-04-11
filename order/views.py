from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from dashboard.models import *
from .models import *
from django.db.models import Sum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TotalOrderAPI(APIView):

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

        transaction_qs = Transaction.objects.filter(order_date__year = int(year), order_date__month__in = qua)
        total_order = len(transaction_qs.values_list('transactionid'))

        response = {
            'total_order':total_order,
        }
        return Response(response)
    

class TotalOrderValueAPI(APIView):

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
        transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        order_value = transaction_qs.aggregate(Sum('amount'))
        total_order_value = order_value['amount__sum'] or 0

        response = {
            'total_order_value':round(total_order_value,2),
        }

        return Response(response)


class TotalAvgOrderValueAPI(APIView):

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
        transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        order_value = transaction_qs.aggregate(Sum('amount'))
        total_order = len(transaction_qs.values_list('transactionid'))
        total_order_value = order_value['amount__sum'] or 0

        avg_order_value = (total_order_value / total_order) * 100

        return Response({
            'total_avg_order_value': round(avg_order_value,2)
        })
    
class TotalOrderReturnRateAPI(APIView):

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
        transaction_qs = Transaction.objects.filter(order_date__year = int(year), order_date__month__in = qua, status = "Delivered")
        total_order = len(transaction_qs.values_list('transactionid'))
        total_order_return = len(transaction_qs.filter(transactionid__in = order_return_id_list).values_list('transactionid'))
        total_order_return_rate = (total_order_return / total_order) * 100

        response = {
            'total_order_return_rate' : round(total_order_return_rate,2)
        }

        return Response(response)
    

class LastSixMonthsOrdersFulFillAPI(APIView):
    
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
            total_order_fulfill_by_tech = len(transaction_qs.filter(productid__category_id = 1).values_list('transactionid'))
            total_order_fulfill_by_sports = len(transaction_qs.filter(productid__category_id = 2).values_list('transactionid'))
            total_order_fulfill_by_stationary = len(transaction_qs.filter(productid__category_id = 3).values_list('transactionid'))

            data = {
                'month_year':month_year,
                'Tech':total_order_fulfill_by_tech,
                'Sports':total_order_fulfill_by_sports,
                'Satationary':total_order_fulfill_by_stationary,
            }
            response.append(data)
        return Response(response)
    

class OrderStatusDistributionAPI(APIView):
    
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
        status_list = transaction_qs.values_list('status',flat=True).distinct()

        response = []
        count = 0
        for i in status_list:
            count += 1
            id = count
            category_name = i
            total_order = len(transaction_qs.filter(status = i))

            data = {
                'id':id,
                'label':category_name,
                'value':total_order,
            }
            response.append(data)

        data1 = {
            'id': count + 1,
            'label':'Return',
            'value':len(transaction_qs.filter(transactionid__in = order_return_id_list)),
        }
        response.append(data1)
        
        return Response(response)