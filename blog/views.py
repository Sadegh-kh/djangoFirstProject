from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView


# Create your views here.

def index_page(request):
    return HttpResponse("index page")


# func base view
# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     posts = paginator.page(page_number)
#     context = {
#         "list_of_post": posts
#     }
#     return render(request, "blog/post_list.html", context)

# class base view
class PostList(ListView):
    queryset = Post.published.all()
    # default is object_list
    context_object_name = "list_of_post"
    paginate_by = 2
    template_name = "blog/post_list.html"


# def post_item(request, id):
#     post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISH)
#     context = {
#         "post": post
#     }
#     return render(request, "blog/post_detail.html", context)

class PostItemDetail(DetailView):
    template_name = "blog/post_detail.html"
    model = Post
