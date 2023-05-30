from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','username','phone_number','password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    
class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Destination
        fields=['name','description','image']

class PackageSerializer(serializers.ModelSerializer):

    destination= serializers.StringRelatedField()

    class Meta:
        model=Package
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2

# class UserPaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPayment
#         fields = ('user', 'payment_id', 'amount', 'status', 'created_at')