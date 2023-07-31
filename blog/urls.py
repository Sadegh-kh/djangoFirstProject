from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('posts/', views.PostList.as_view(), name="post_list"),
    path('posts/<pk>', views.post_item, name="post_item"),
    path('posts/<pk>/comment', views.post_comment, name="post_comment"),
    path("ticket/", views.ticket, name="ticket"),
    path("posts/new_post/create", views.create_post, name="create_post"),
    path("posts/new_post/create/<pk>", views.edit_post, name="edit_post"),
    path("posts/delete_image/<pk>", views.delete_image, name="delete_image"),
    path("posts/delete_post/<pk>", views.delete_post, name='delete_post'),
    path("search/", views.post_search, name="post_search"),
    path("profile/", views.profile, name="profile"),
]
