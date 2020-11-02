from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Post
from django.utils import timezone
from notifications.signals import notify 

from django.contrib.auth.decorators import login_required

def main(request):
    return render(request, 'main.html')

# 회원 가입
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            return redirect('/')
    return render(request, 'signup.html')

# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

# 로그 아웃
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    return render(request, 'login.html')

def new(request):
    return render(request, 'new.html')

def mypage(request):
    recipients = User.objects.all()
    user = request.user
    if user in recipients:
        unread_messages = user.notifications.unread()
        return render(request, 'mypage.html',{'unread_messages':unread_messages})
    return render(request, 'mypage.html')

def create(request):
    recipients = User.objects.all()  #알림 받을 사람들
    post = Post()
    post.title = request.GET['title']
    post.content = request.GET['content']
    post.pub_date = timezone.datetime.now()
    post.save()
    notify.send(request.user, recipient = recipients, verb ='님 께서 새로운 글을 작성하셨습니다')
    return redirect('post')

def post(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        user = request.user
        user.notifications.mark_all_as_read()
    return render(request, 'post.html', {'posts': posts})