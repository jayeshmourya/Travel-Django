# websocket_app/consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'notifications'
        print('connectttttttt')

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Process received data if needed
        pass

    # Method to send notification to the connected WebSocket clients
    def send_notification(self, event):
        notification = event['notification']
        print('senddddddddddnotiffffication')

        # Send notification to WebSocket
        self.send(text_data=json.dumps({
            'notification': notification
        }))




  
        
