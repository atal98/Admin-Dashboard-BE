from rest_framework import serializers
from dashboard.models import UsersInfo

class UsersTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersInfo
        fields = ('userid' ,'user_name', 'city', 'state', 'age','phone','email','gender')