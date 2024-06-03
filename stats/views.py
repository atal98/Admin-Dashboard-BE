from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from dashboard.models import *
from .models import *
from django.db.models import Sum,F
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CACAPI(APIView):
    permission_classes = [IsAuthenticated]

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

        
        user_qs = UsersInfo.objects.all()
        sale_and_marketing = SalesAndMarketing.objects.filter(quarter= int(quarter), year= int(year))
        customer_acquired = len(user_qs.filter(cr_dt__year = int(year), cr_dt__month__in = qua))
        total_expense = sale_and_marketing.first().total_expense if sale_and_marketing else 0

        cac = total_expense / customer_acquired if customer_acquired > 0 else 0
        # print(total_expense, customer_acquired)
        response = {
            "cac" : round(cac)
        }
        return Response(response)
    

class SalesExpenseVSCustomerAcqVSTotalLeadsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
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

        user_qs = UsersInfo.objects.all()
        sale_and_marketing_qs = SalesAndMarketing.objects.filter(quarter= int(quarter), year= int(year))
        lead_qs = Leads.objects.filter(quarter= int(quarter), year= int(year))

        
        ads_leads = lead_qs.aggregate(Sum('ads_leads'))
        email_leads = lead_qs.aggregate(Sum('email_leads'))
        refferal_leads = lead_qs.aggregate(Sum('refferal_leads'))
        social_media = lead_qs.aggregate(Sum('social_media'))
        trade_show_leads = lead_qs.aggregate(Sum('trade_show_leads'))

        total_leads = ads_leads['ads_leads__sum'] if ads_leads['ads_leads__sum'] else 0 + email_leads['email_leads__sum'] if email_leads['email_leads__sum'] else 0 + refferal_leads['refferal_leads__sum'] if refferal_leads['refferal_leads__sum'] else 0 + social_media['social_media__sum'] if social_media['social_media__sum'] else 0 + trade_show_leads['trade_show_leads__sum'] if trade_show_leads['trade_show_leads__sum'] else 0
        Total_customer_acquired = len(user_qs.filter(cr_dt__year = int(year), cr_dt__month__in = qua))
        total_expense = sale_and_marketing_qs.get().total_expense if sale_and_marketing_qs else 0

        response = [{
            'Year_Qua':f"{year}/{quarter}",
            'Total_Leads':total_leads,
            'Total_Customer_Acquired':Total_customer_acquired,
            'Total_Expense':round(total_expense/100000),
        }]
        
        return Response(response)

class SalesExpenseBreakDownAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)

        sale_and_marketing_qs = SalesAndMarketing.objects.filter(quarter= int(quarter), year= int(year))

        ads = sale_and_marketing_qs.aggregate(Sum('ads'))
        salaries = sale_and_marketing_qs.aggregate(Sum('salaries'))
        content_creation = sale_and_marketing_qs.aggregate(Sum('content_creation'))
        other_expense = sale_and_marketing_qs.aggregate(Sum('other_expense'))

        response = [
            {
                'id':1,
                'label':"Ads",
                'value':ads["ads__sum"]/100000 if ads["ads__sum"] else 0,
            },
            {
                'id':2,
                'label':"Salaries",
                'value':salaries["salaries__sum"]/100000 if salaries["salaries__sum"] else 0,
            },
            {
                'id':3,
                'label':"Content Creation",
                'value':content_creation["content_creation__sum"]/100000 if content_creation["content_creation__sum"] else 0,
            },
            {
                'id':4,
                'label':"Other Expenses",
                'value':other_expense["other_expense__sum"]/100000 if other_expense["other_expense__sum"] else 0,
            },
        ]
        return Response(response)


class NetProfitBreakdownAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)

        if int(quarter) == 1:
            qua = [1,2,3]
            month = ['January','Febuary','March']
        elif int(quarter) == 2:
            qua = [4,5,6]
            month = ['April','May','June']
        elif int(quarter) == 3:
            qua = [7,8,9]
            month = ['July','August','September']
        elif int(quarter) == 4:
            qua = [10,11,12]
            month = ['October','November','December']
        
        total_revenue = []
        gross_profit = []
        ads = []
        salaries = []
        content_creation = []
        other_expense = []
        net_profit = []

        for i in qua:
            
            #revenue
            order_return_id_list = TransactionInfo.objects.filter(status = 'Refunded').values_list('transactionid',flat=True)
            transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month = i, status = "Delivered")
            amount = transaction_qs.aggregate(Sum('amount'))
            total_revenue.append(amount['amount__sum'] or 0)

            # Annotate transactions with the cost_making_or_buying from ProductInfo
            annotated_transactions = transaction_qs.annotate(cogs_amount=F('productid__productinfo__amount'))
            cogs = annotated_transactions.aggregate(total_cogs=Sum(F('cogs_amount') * F('qty')))['total_cogs'] if annotated_transactions.aggregate(total_cogs=Sum(F('cogs_amount') * F('qty')))['total_cogs'] else 0
            
            gross_profit.append((amount['amount__sum'] or 0) - cogs)

            #sales expenses
            sale_and_marketing_qs = SalesAndMarketing.objects.filter(quarter= int(quarter), year= int(year))
            ads.append(round((sale_and_marketing_qs.get().ads/3 if sale_and_marketing_qs else 0),2))
            salaries.append(round((sale_and_marketing_qs.get().salaries/3 if sale_and_marketing_qs else 0),2))
            content_creation.append(round((sale_and_marketing_qs.get().content_creation/3 if sale_and_marketing_qs else 0),2))
            other_expense.append(round((sale_and_marketing_qs.get().other_expense/3 if sale_and_marketing_qs else 0),2))

            #Net profit
            total_expense = round((sale_and_marketing_qs.get().ads/3 if sale_and_marketing_qs else 0),2) + round((sale_and_marketing_qs.get().salaries/3 if sale_and_marketing_qs else 0),2) + round((sale_and_marketing_qs.get().content_creation/3 if sale_and_marketing_qs else 0),2) + round((sale_and_marketing_qs.get().other_expense/3 if sale_and_marketing_qs else 0),2)

            net_profit.append((amount['amount__sum'] or 0) - cogs - total_expense)

        response = {
            "labels": month,
            "datasets": [
                {
                "label": "Revenue",
                "data": total_revenue,
                },
                {
                "label": "Gross Profit",
                "data": gross_profit,
                },
                {
                "label": "Ads Expense",
                "data": ads,
                },
                {
                "label": "Salaries Expense",
                "data": salaries,
                },
                {
                "label": "Content Creation Expense",
                "data": content_creation,
                },
                {
                "label": "Other Expense",
                "data": other_expense,
                },
                {
                "label": "Net Profit",
                "data": net_profit,
                },
            ],
        }
        return Response(response)
    
class GrowthRateAPI(APIView):
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
        response =[]

        count = 0
        for i in qua:
            count += 1
            id = count
            transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = int(year), order_date__month = i, status = "Delivered")
            amount = transaction_qs.aggregate(Sum('amount'))
            total_revenue = amount['amount__sum'] or 0

            if int(year) == 2021 and i == 1 :
                prev_month = i
                prev_year = year
            else:
                quarter_start_date = datetime(int(year), i, 1)
                previous_months_start_date = quarter_start_date - relativedelta(months=1)
                prev_month = previous_months_start_date.month
                prev_year = previous_months_start_date.year
            
            prev_month_transaction_qs = Transaction.objects.exclude(transactionid__in = order_return_id_list).filter(order_date__year = prev_year, order_date__month = prev_month, status = "Delivered")
            prev_amount = prev_month_transaction_qs.aggregate(Sum('amount'))
            prev_total_revenue = prev_amount['amount__sum'] or 0

            
            percent = (total_revenue - prev_total_revenue) / prev_total_revenue
            data = {
                
                'id':id,
                'label':calendar.month_name[i],
                'value':round(abs(percent*100), 2),
                'percent': round(percent*100, 2),
                'revenue': total_revenue,
            }
            response.append(data)


        return Response(response)

        