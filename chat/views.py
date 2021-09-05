from django.shortcuts import render

# Create your views here.


def room(request, room_name):
    return render(request, "chatroom.html", {"room_name": room_name})


def index(request):
    return render(request, "index.html", {})
