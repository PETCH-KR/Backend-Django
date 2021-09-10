from channels.generic.websocket import AsyncWebsocketConsumer
import json

"""
Route 를 통하여 Consumer에 접근

urls -> views
routing -> consumers
"""


class ChatRoomConsumer(AsyncWebsocketConsumer):
    # Start connection
    async def connect(self):  # calling it will return coroutine(?) object
        """
        enabling web socket activity
        """

        # extract room name
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # setup group room name
        self.room_group_name = "chat_%s" % self.room_name

        # Construct group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,  # contains pointer to the channel layer isntance & name to reach the consumer
        )

        # Accept socket connection
        await self.accept()

        # need a broker --> config.settings CHANNEL_LAYERS

    #     # send message to the group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {"type": "tester_message", "tester": "someone new joined"},
    #     )

    # async def tester_message(self, event):
    #     # collect data from the gropup_send
    #     tester = event["tester"]

    #     # send the messgae
    #     await self.send(text_data=json.dumps({"tester": tester}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chatroom_message", "message": message, "username": username},
        )

    async def chatroom_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps({"username": username, "message": message})
        )
