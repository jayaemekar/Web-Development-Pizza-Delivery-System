from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync
from .bot_messages import BOT_MESSAGES


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connected')
        self.accept()
        self.bot_message = "Hi, welcome to Cal Pizza Delivery System! Please share your Order ID"
        self.send(text_data=json.dumps({
            'bot_message': self.bot_message
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.bot_message)
        if self.bot_message in [BOT_MESSAGES.get("Welcome"),BOT_MESSAGES.get("incorrect_order_id")]:
            try:
                order = Order.objects.filter(order_id=message).first()
                print(order)
                order_user_full_name = order.user.first_name + ' ' + order.user.last_name
                self.bot_message = "Welcome {}.\n".format(order_user_full_name)+"\n"
                self.bot_message += BOT_MESSAGES.get("first_question")
            except Exception:    
                if self.talk_to_bot(message):
                    self.bot_message = BOT_MESSAGES.get("incorrect_order_id")
            print(self.bot_message)
        elif BOT_MESSAGES.get("first_question") in self.bot_message:
            if message.lower() in ["1", "expedite order process", "order"]:
                self.bot_message = BOT_MESSAGES.get("expedition_request")
                self.bot_message += "Thank you for connecting with us.\n"
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            elif message.lower() in ["2", "track my order", "track"]:
                self.bot_message = BOT_MESSAGES.get("order_id")
            else:
                self.bot_message = BOT_MESSAGES.get("first_question")            

        elif self.bot_message == BOT_MESSAGES.get("order_id"):
            print(Order.objects.filter(order_id=message).values('status'))
            try:
                order_status = Order.objects.filter(order_id=message).values('status')
                self.bot_message = "Your order status is {}.\n".format((order_status[0]).get('status'))
                self.bot_message += BOT_MESSAGES.get("thanks-bye")
            except Exception:
                self.bot_message = BOT_MESSAGES.get("invalid_order")

        else:
            if self.talk_to_bot(message):
                self.bot_message = BOT_MESSAGES.get("Welcome")

        self.send(text_data=json.dumps({
            'bot_message': self.bot_message,
            'user_message': message
        }))

    def talk_to_bot(self, message):
        if message.lower() in BOT_MESSAGES.get("user-hello"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-hello"))
        elif message.lower() in BOT_MESSAGES.get("user-whatsup"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-whatsup"))
        elif message.lower() in BOT_MESSAGES.get("user-bye"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-bye"))
        elif message.lower() in BOT_MESSAGES.get("user-greeting"):
            self.bot_message = random.choice(BOT_MESSAGES.get("bot-greeting"))
        else:
            return True




class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.accept())
        order = Order.get_order_detail(self.room_name)

        self.send(text_data=json.dumps({
            'status': 'Backend Consumer (Websocket): Connected',
            'payload': order,
        }))
    
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data,
            }
        )

    def order_status(self, event):
        order = json.loads(event.get('value'))
        self.send(text_data=json.dumps({
            'payload': order
        }))

    def disconnect(self, *args, **kwargs):
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        ) 
        pass

