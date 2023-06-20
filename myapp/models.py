from django.db import models
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    image=models.FileField(upload_to='users',blank=True,null=True)



class Notification(models.Model):
    message = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notifications', {
            'type': 'send_notification',
            'notification': self.message
        })
    

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='destinations',blank=True,null=True)

    def __str__(self):
        return self.name
    
class Picture(models.Model):
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    pic=models.FileField(upload_to='',blank=True,null=True)

    
    

class Package(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_journey_date=models.DateTimeField()
    end_journey_date=models.DateTimeField()
    start_location=models.CharField(max_length=50)
    end_location=models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product
    


