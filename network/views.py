from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post

POST_PER_PAGE = 10 


def index(request):
    posts = Post.objects.all().order_by('-posted_on')
    paginator = Paginator(posts, POST_PER_PAGE)    

    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1

    posts_page = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'posts_page': posts_page,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def new_post(request):
    ''' takes a request and a post field text and stores that text in the database if it is under 300 characters'''
    if request.method == "POST":
        # accessing the user and the text
        user = request.user
        text = request.POST.get('text')
        if text == '':
            return render(request, 'network/index.html', {
                'message': 'Please enter a text to post'
            })
        try:
            post = Post(text=text, user=user)
            post.save()
        except IntegrityError:
            return render(request, 'network/index.html', {
                'message': 'Error During posting please try again'
            })
    return HttpResponseRedirect(reverse('index')) 

def user_view(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-posted_on')
    pagination = Paginator(posts, POST_PER_PAGE)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    posts_page = pagination.get_page(page_number)
    return render(request, 'network/userview.html', {
       'posts_page': posts_page, 
       'queried_user':user,
    })

def following(request, username):
    user = User.objects.get(username=username)
    following = user.following.all()
    return render(request, 'network/followingfollowers.html', {
        'queried_user':user,
        'user_list':following,
        'following':True,
    })

def followers(request, username):
    user = User.objects.get(username=username)
    followers = user.followers.all()
    return render(request, 'network/followingfollowers.html', {
        'queried_user':user,
        'user_list':followers,
        'followers':True,
    })

@login_required(login_url='login')
def following_posts(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(user__in=following_users)
    paginator = Paginator(posts, POST_PER_PAGE)
    
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    
    posts_page = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'posts_page': posts_page,
    })

def follow_unfollow_view(request, queried_username):
    if request.method == 'POST':
        user = request.user
        queried_user = User.objects.get(username=queried_username)
        user.follow_unfollow(queried_user)
    return HttpResponseRedirect(reverse('user-view', args=[queried_username]))

@login_required(login_url='login')
def edit(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('postId')
        new_text = request.POST.get('newText')
        if new_text is None or new_text == '':
            pass
            #TODO
        if post_id is None:
            #TODO
            pass
        post = Post.objects.get(pk=post_id)
        if user != post.user:
            #TODO
            pass
        try:
            post.text = new_text
            post.save()
        except IntegrityError:
            #TODO
            pass
        return HttpResponse(status=200)

@login_required(login_url='login')
def like_unlike(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('postId')
        if post_id is None:
            #TODO
            pass
        try:
            post = Post.objects.get(pk=post_id)
            print(post_id)
            if user == post.user:
                #TODO
                return HttpResponse(status=404)
            user.like_dislike(post)
        except IntegrityError:
            #TODO
            return HttpResponse(status=404)

        return JsonResponse({'likes': post.liked_by.count()}, status=200)