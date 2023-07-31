from django.urls import path
from .views import *

app_name = "blog"
urlpatterns = [
    path('posts/', PostList.as_view(), name="post_list"),
    path('posts/<pk>', post_item, name="post_item"),
    path('posts/<pk>/comment', post_comment, name="post_comment"),
    path("ticket/", ticket, name="ticket"),
    path("posts/new_post/create", create_post, name="create_post"),
    path("posts/new_post/create/<pk>", edit_post, name="edit_post"),
    path("posts/delete_image/<pk>", delete_image, name="delete_image"),
    path("posts/delete_post/<pk>", delete_post, name='delete_post'),
    path("search/", post_search, name="post_search"),
    path("profile/", profile, name="profile"),
]
