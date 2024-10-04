from django.urls import path, include
import users.views as user_views
import directchat.views as chat_views

urlpatterns = [
    path('', user_views.profile, name='profile'),
    path('messages/', include('directchat.urls'), name='directchat'),
    path('groups/', user_views.groups, name='groups'),
    path('data/', user_views.data, name='data'),
    path('user/<str:username>/', user_views.user_profile, name='user-profile')
]