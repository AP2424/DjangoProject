from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, \
join_fanclub, leave_fanclub, FanClubsView, fanclub_main



urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('join/<str:fanclub_name>/', join_fanclub, name='join-fanclub'),
    path('leave/<str:fanclub_name>/', leave_fanclub, name='leave-fanclub'),
    path('fanclubs/', FanClubsView.as_view(), name='fanclubs'),
    path('fanclub/<str:fanclub_name>/', fanclub_main, name='fanclub-main')
]