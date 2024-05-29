from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from dashboard.models import *
from user.serializers import UsersTableSerializer
from .models import *
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.
class UserTableAPI(APIView):

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

        
        user_qs = UsersInfo.objects.filter(cr_dt__year = int(year), cr_dt__month__in = qua)
        serializer = UsersTableSerializer(user_qs, many=True)

        return Response(serializer.data)


class UserSinigleAPI(APIView):

    def get(self, request, pk=None):
        
        queryset = UsersInfo.objects.get(userid=pk)
        serializer = UsersTableSerializer(queryset, many=False)
        return Response(serializer.data)

    

class TotalRetentionRateAPI(APIView):

    def get(self,request):

        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)
        quarter_start_date = datetime(int(year), (int(quarter) - 1) * 3 + 1, 1)

        if int(quarter) == 1:
            qua = [1,2,3]
        elif int(quarter) == 2:
            qua = [4,5,6]
        elif int(quarter) == 3:
            qua = [7,8,9]
        elif int(quarter) == 4:
            qua = [10,11,12]

        
        user_qs = UsersInfo.objects.all()
        customer_acquired = len(user_qs.filter(cr_dt__year = int(year), cr_dt__month__in = qua))
        customer_at_start = len(UsersInfo.objects.filter(cr_dt__lt=quarter_start_date))
        customer_at_end = customer_at_start + customer_acquired
        user_rention_rate = ((customer_at_end - customer_acquired) / customer_at_start) * 100 if customer_at_start > 0 else 0

        response = {
            'total_user_rention_rate': round(user_rention_rate,2)
        }

        return Response(response)


class TotalChurnRateAPI(APIView):

    def get(self,request):

        return Response({
            'total_user_churn_rate': 0
        })
    
class TotalConversionRateAPI(APIView):

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
        leads_qs = Leads.objects.filter(year= int(year),quarter = int(quarter))

        customer_acquired = len(user_qs.filter(cr_dt__year = int(year), cr_dt__month__in = qua))
        ads_leads = leads_qs.aggregate(Sum('ads_leads'))
        email_leads = leads_qs.aggregate(Sum('email_leads'))
        refferal_leads = leads_qs.aggregate(Sum('refferal_leads'))
        social_media = leads_qs.aggregate(Sum('social_media'))
        trade_show_leads = leads_qs.aggregate(Sum('trade_show_leads'))

        total_leads = ads_leads['ads_leads__sum'] if ads_leads['ads_leads__sum'] else 0 + email_leads['email_leads__sum'] if email_leads['email_leads__sum'] else 0 + refferal_leads['refferal_leads__sum'] if refferal_leads['refferal_leads__sum'] else 0 + social_media['social_media__sum'] if social_media['social_media__sum'] else 0 + trade_show_leads['trade_show_leads__sum'] if trade_show_leads['trade_show_leads__sum'] else 0
        total_user_conversin_rate = (customer_acquired / total_leads) * 100 if total_leads > 0 else 0

        response = {
            'total_user_conversin_rate' : round(total_user_conversin_rate,2)
        }

        return Response(response)