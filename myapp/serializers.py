from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email','username','phone_number','image','password']

        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user   

    def update(self, instance, validated_data):
        # Hash the password before saving
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password.')
        return value

    def validate_new_password(self, value):
        return make_password(value)
    
    
class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Destination
        fields=['name','description','image']

class PictureSerializer(serializers.ModelSerializer):
    destination=serializers.StringRelatedField()
    class Meta:
        model=Picture
        fields='__all__'


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
