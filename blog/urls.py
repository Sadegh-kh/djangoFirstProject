from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('posts/', views.post_list, name="post_list"),
    path('posts/<str:category>', views.post_list, name="post_list_category"),
    path('posts/detail/<pk>', views.post_item, name="post_item"),
    path('posts/<pk>/comment', views.post_comment, name="post_comment"),
    path("ticket/", views.ticket, name="ticket"),
    path("posts/new_post/create", views.create_post, name="create_post"),
    path("posts/new_post/create/<pk>", views.edit_post, name="edit_post"),
    path("posts/delete_image/<pk>", views.delete_image, name="delete_image"),
    path("posts/delete_post/<pk>", views.delete_post, name='delete_post'),
    path("search/", views.post_search, name="post_search"),
]
