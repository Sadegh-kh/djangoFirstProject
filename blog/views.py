from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.views.decorators.http import require_POST
from django.db.models import Avg, Max, Min


# Create your views here.

def index_page(request):
    aggregate_post = Post.published.aggregate(Avg("reading_time"), Max("reading_time"), Min("reading_time"))
    context = {
        'max_time': aggregate_post['reading_time__max'],
        'min_time': aggregate_post['reading_time__min'],
        'avg_time': aggregate_post['reading_time__avg'],
    }
    return render(request, 'blog/index.html',context)


# func base view
# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     # for example we have 4 object , user enter 5 and Paginator rise EmptyPage
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
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


def post_item(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISH)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {
        "post": post,
        'form': form,
        'comments': comments,
    }
    return render(request, "blog/post_detail.html", context)


# class PostItemDetail(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISH)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.message = cd['message']
            ticket_obj.save()
            return redirect("blog:home")
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form': form})
