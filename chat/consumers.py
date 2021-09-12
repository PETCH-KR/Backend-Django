from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.forms.models import model_to_dict
from server.serializers.chatroom_serializer import ChatroomSerializer
from server.models import Chatroom, Organization, User, AbstractMessage, chatroom_model
from server.utils.json_util import jsonify
from channels.db import database_sync_to_async
from bson import ObjectId
from copy import deepcopy as deepcopy
import datetime
import time

@database_sync_to_async
def save_to_database(group_name, sender, messageType, message):
    try:
        chatroom = Chatroom.objects.get(room_name=group_name)
    except:
        user = group_name.split("_")[1]
        org = group_name.split("_")[2]
        
        print(user, org)
        user = model_to_dict(User.objects.get(_id=ObjectId(user)))
        org = model_to_dict(Organization.objects.get(_id=ObjectId(org)))
        data = jsonify({"room_name": group_name, "user":user, "organization":org, "message":[]})
        serializer = ChatroomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            chatroom = Chatroom.objects.get(room_name=group_name)
        else:
            print(serializer.errors)


    new_message = {"sender":sender, "messageType":messageType, "message":message, "createAt":datetime.datetime.fromtimestamp(time.time())}

    chatroom.message.append(new_message)

    chatroom.save()
    
    
    # data = model_to_dict(chatroom)

    # serializer = ChatroomSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else:
    #     serializer.errors()

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
        messageType = event["type"]

        await self.send(
            text_data=json.dumps({"username": username, "message": message})
        )
        await save_to_database(self.room_group_name, username, messageType, message)

