from django.urls import path
from .views import messages, join_room, leave_room, search

urlpatterns = [
    path('', messages, name='messages'),
    path('join/<str:des_username>/', join_room, name='join-room'),
    path('leave/<str:room_name>/', leave_room, name='leave-room'),
    path('search/<str:query>/', search, name='users-search')
]