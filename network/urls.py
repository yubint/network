
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new-post"),
    path("user/<str:username>", views.user_view, name="user-view"),
    path("user/<str:username>/following", views.following, name="following"),
    path("user/<str:username>/followers", views.followers, name="followers"),
    path("following-posts", views.following_posts, name="following-posts"),
    path("follow-unfollow/<str:queried_username>", views.follow_unfollow_view, name="follow-unfollow"),
    path("edit", views.edit, name="edit"),
    path("like-unlike", views.like_unlike, name="like-unlike"),
]
