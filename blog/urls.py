from django.urls import path
from .views import *

app_name = "blog"
urlpatterns = [
    path("", index_page, name="home"),
    path('posts/', PostList.as_view(), name="post_list"),
    path('posts/<pk>', PostItemDetail.as_view(), name="post_item"),
    path("ticket/", ticket, name="blog-ticket")
]
