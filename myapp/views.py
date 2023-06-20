from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import filters,status,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from rest_framework import viewsets
import razorpay

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.hashers import make_password


class CustomUserView(ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


    def update_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['put','post','get'])
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        print(user.username)

        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    





    @action(detail=False, methods=['post'])
    def login(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Return a success response or the authenticated user data
            return Response({'message': 'Login successful'})
        else:
            # Return an error response indicating invalid credentials
            return Response({'message': 'Invalid username/email or password'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logoutsuccessful'})


class DestinationView(ModelViewSet):

    queryset=Destination.objects.all()
    serializer_class=DestinationSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name']



    
    def dispatch(self, request, *args, **kwargs):
        # Run a function before the viewset is called
        self.send_notification()

        return super().dispatch(request, *args, **kwargs)     

    def list(self, request,*args, **kwargs):
        search_query = request.GET.get('search', '')
        queryset = self.filter_queryset(self.get_queryset())

       
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    

    def send_notification(notification):
                channel_layer = get_channel_layer()
                print('send notidjfnjd viewwwww')
                async_to_sync(channel_layer.group_send)('notifications', {
                    'type': 'send_notification',
                    'notification': 'jayesh'
                })

class PicturesView(ModelViewSet):
    queryset=Picture.objects.all()
    serializer_class=PictureSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['destination__name']




class PackageView(ModelViewSet):
    queryset=Package.objects.all()
    serializer_class=PackageSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['destination__name']





import json


import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer



# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']
    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=('rzp_test_Yta8TIBl3IRFDl', 'W5PaF8qwmMw4Qnu0GESMo436'))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    print('successsssssssssssssssssssss')
    # request.data is coming from frontend
    res = json.loads(request.data["response"])
    print(res)

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
            
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=('rzp_test_Yta8TIBl3IRFDl', 'W5PaF8qwmMw4Qnu0GESMo436'))

    

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None

    
    # print('dataaaaaaaaaaaaaaaaaaaaaaaaa',data['razorpay_order_id'])
    # data['razorpay_order_id']='order_Lz6XYVYL9Qvz6jj'
    # print('dataaaaaaaaaaaaaaaaaaaaaaaaa',data['razorpay_order_id'])
    
    check = client.utility.verify_payment_signature(data)

    print('checkkkkkkkkkkk',check)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)


