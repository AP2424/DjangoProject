from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import ChatRoom, Message
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.models import Profile
import search_algorithms as sl
from django.utils import timezone
from django.conf import settings

def testview(request):
    return render(request, template_name='directchat/main.html')

def join_room(request, des_username):
    user = request.user
    des_user = User.objects.get(username=des_username)
    if user == des_user:
        return
    usernames = sorted([request.user.username, des_user.username])
    room_name = ''.join(usernames)
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    room.users.add(*[user, des_user])
    messages = Message.objects.filter(room=room)
    lastmessages = []
    endusers = []
    activities = []
    for room in ChatRoom.objects.all():
        users = room.users.all()
        if request.user in users:
            in_messages = Message.objects.filter(room=room)
            if in_messages:
                enduser = [user for user in users if user != request.user][0]
                lastmessages.append(in_messages.last().text)
                endusers.append(enduser)
                active_period = settings.ACTIVE_USER_PERIOD
                nonactive_timeframe = timezone.now() - enduser.profile.last_activity
                if active_period > nonactive_timeframe:
                    activities.append('active')
                else:
                    activities.append(str(nonactive_timeframe))

    chats = zip(endusers, lastmessages, activities)
    if request.method == "POST":
        deleteid = request.POST.get('delete')
        print(deleteid)
        if deleteid:
            message = Message.objects.get(id=deleteid)
            message.delete()
        return redirect(request.path)
    return render(request, template_name='directchat/chatroom.html',
                  context={'room_name': room_name,
                           'enduser': des_user,
                           'messages': messages,
                           'chats': chats})


def leave_room(request, room_name):
    user = request.user
    room = get_object_or_404(ChatRoom, name=room_name)
    room.delete()
    return JsonResponse({'status': 'left'})

def messages(request):
    if request.method == "POST":
        query = request.POST.get('query')
        return redirect('users-search', query=query)
    endusers = []
    lastmessages = []
    for room in ChatRoom.objects.all():
        users = room.users.all()
        if request.user in users:
            messages = Message.objects.filter(room=room)
            if messages:
                lastmessages.append(messages.last().text)
                endusers.append([user for user in users if user != request.user][0])
    chats = zip(endusers, lastmessages)
    return render(request, 'directchat/messages.html', context={'chats': chats})

def search(request, query):
    matched_users = []
    for letter in query:
        if letter in sl.keyboard_ru_en.keys():
            modquery = query.replace(letter, sl.keyboard_ru_en[letter])
            query = modquery
    for user in User.objects.all():
        if query.lower() in user.username.lower():
            matched_users.append(user)
    return render(request, 'directchat/search.html', context={'users': matched_users})



