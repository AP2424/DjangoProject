from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post
from fantasy.models import Team
from .models import FanClub
from directchat.models import Message
from django.conf import settings
from django.utils import timezone


def home(request):
	return render(request, 'blog/home.html', {'my_posts': Post.objects.all()})

def join_fanclub(request, fanclub_name):
	user = request.user
	fanclub = get_object_or_404(FanClub, team=Team.objects.get(name=fanclub_name))
	fanclub.users.add(user)
	JsonResponse({'status': 'joined'})
	return redirect(reverse('fanclub-main', kwargs={'fanclub_name': fanclub_name}))

def leave_fanclub(request, fanclub_name):
	user = request.user
	fanclub = get_object_or_404(FanClub, team=Team.objects.get(name=fanclub_name))
	fanclub.users.remove(user)
	return redirect('fanclubs')

def fanclub_main(request, fanclub_name):
	fanclub = FanClub.objects.get(team=Team.objects.get(name=fanclub_name))
	messages = Message.objects.filter(room=fanclub)
	users = fanclub.users.all()
	active_users = []
	active_period = settings.ACTIVE_USER_PERIOD
	for user in users:
		nonactive_timeframe = timezone.now() - user.profile.last_activity
		if active_period > nonactive_timeframe:
			active_users.append(user)
	active_users.remove(request.user)
	if (request.user not in fanclub.users.all()):
		return redirect(reverse('join-fanclub', kwargs={'fanclub_name': fanclub_name}))
	return render(request, 'blog/fanclubchat.html', {'fanclub': fanclub,
													 'messages': messages,
													 'users': active_users})

class FanClubsView(ListView):
	model = FanClub
	template_name = 'blog/fanclubs.html'
	context_object_name = 'fanclubs'
	paginate_by = 30
	def get_queryset(self):
		return FanClub.objects.order_by('-users')


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'my_posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'my_posts'
	paginate_by = 5
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post = self.get_object()
		tags = post.post_tags.all()
		comments = post.comments.all()
		commentsNum = len(comments)
		context['tags'] = tags
		context['comments'] = comments
		context['commentsNum'] = commentsNum
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'post_tags']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'post_tags']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

