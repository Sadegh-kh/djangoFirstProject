from django.urls import path
from .views import *

app_name = "blog"
urlpatterns = [
    path("", index_page, name="home"),
    path('posts/', post_list, name="post_list"),
    path('posts/<int:id>', post_item, name="post_item"),
]
