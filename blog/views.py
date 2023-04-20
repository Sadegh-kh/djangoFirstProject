from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Post


# Create your views here.

def index_page(request):
    return HttpResponse("index page")


def post_list(request):
    posts = Post.published.all()
    context = {
        "posts": posts
    }
    return render(request, "post_list.html", context)


def post_item(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404("Post NotFound")
    context = {
        "post": post
    }
    return render(request, "post_detail.html", context)
