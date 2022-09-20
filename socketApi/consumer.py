import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.room_id  = self.scope["url_route"]["kwargs"]["chat_room_id"]
        self.room_group_name = "chat_%s" % self.room_id

    async def connect(self):
        try:
            await self.channel_layer.group_add( 
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"CONNECTED ------> CHANNEL_NAME: {self.channel_name}" )
        except Exception as e:
            print("Socket Connection Failed")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            response = text_data_json
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type":"broadcast.message",
                    "response":response
                }
            )
        except Exception as e:
            await self.send_json( 
                {
                    "response":"Invalid data format"
                }
            )
        
    async def broadcast_message(self, event):
        response = event["response"]
        await self.send_json(response)
    

            
     