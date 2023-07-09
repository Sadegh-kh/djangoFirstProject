from django.urls import path
from .views import *

app_name = "blog"
urlpatterns = [
    path("", index_page, name="home"),
    path('posts/', PostList.as_view(), name="post_list"),
    path('posts/<pk>', post_item, name="post_item"),
    path('posts/<pk>/comment', post_comment, name="post_comment"),
    path("ticket/", ticket, name="ticket")
]
