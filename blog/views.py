from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post


# Create your views here.

def index_page(request):
    return HttpResponse("index page")


def post_list(request):
    posts = Post.published.all()
    context = {
        "list_of_post": posts
    }
    return render(request, "blog/post_list.html", context)


def post_item(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISH)
    context = {
        "post": post
    }
    return render(request, "blog/post_detail.html", context)
