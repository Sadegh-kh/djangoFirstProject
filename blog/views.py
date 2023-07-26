from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket, Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.views.decorators.http import require_POST
from django.db.models import Avg, Max, Min
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity, SearchHeadline


# Create your views here.

def index_page(request):
    aggregate_post = Post.published.aggregate(Avg("reading_time"), Max("reading_time"), Min("reading_time"))
    context = {
        'max_time': aggregate_post['reading_time__max'],
        'min_time': aggregate_post['reading_time__min'],
        'avg_time': aggregate_post['reading_time__avg'],
    }
    return render(request, 'blog/index.html', context)


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


def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.auther = request.user
            post_form.save()

            # method 2  for autofill slug field
            # post_form.slug = f"{user_id}-{form.cleaned_data['title']}"

            Image.objects.create(image_file=form.cleaned_data['image1'], description=form.cleaned_data['description'],
                                 title=form.cleaned_data['title'], post=post_form)
            Image.objects.create(image_file=form.cleaned_data['image2'], description=form.cleaned_data['description'],
                                 title=form.cleaned_data['title'], post=post_form)
            return redirect("blog:profile")

    else:
        form = PostForm()
    context = {
        "form": form
    }

    return render(request, "forms/post.html", context)


def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile")
    context = {
        'post': post
    }
    return render(request, 'forms/delete-post.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    images = post.images.all()
    print(images)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            if form.cleaned_data['image1']:
                Image.objects.create(description=form.cleaned_data['description'],
                                     title=form.cleaned_data['title'],
                                     post=post, image_file=form.cleaned_data['image1'])
            elif form.cleaned_data['image2']:
                Image.objects.create(description=form.cleaned_data['description'],
                                     title=form.cleaned_data['title'],
                                     post=post, image_file=form.cleaned_data['image2'])

        if images_count := images.count() > 0:
            for i in range(1, images_count + 1):
                image_id = request.POST.get(f'image-id-{i}')
                new_image = request.FILES.get(f'image - {i}')
                try:
                    image = Image.objects.get(id=image_id)
                    image.image_file = new_image
                    image.save()
                except:
                    if new_image:
                        Image.objects.create(description=form.cleaned_data['description'],
                                             title=form.cleaned_data['title'],
                                             post=post, image_file=new_image)
                    else:
                        Image.objects.create(description=form.cleaned_data['description'],
                                             title=form.cleaned_data['title'],
                                             post=post, image_file=Image.objects.get(id=image_id))

            return redirect('blog:profile')
    else:
        form = PostForm(instance=post)
    context = {
        'post': post,
        'images': images,
        'form': form
    }
    return render(request, "forms/post.html", context)


def delete_image(request, pk):
    image = get_object_or_404(Image, id=pk)
    post_id = image.post.id
    image.delete()
    return redirect('blog:edit_post', pk=post_id)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search with search query and search vector and search rank
            # search_query = SearchQuery(query)
            # search_vector = SearchVector('title', weight="A") + SearchVector('description', weight="B")
            # rank = SearchRank(search_vector, search_query, weights=[0.1, 0.3, 0.6, 0.9])
            # results = Post.published.annotate(search=search_vector, rank=rank) \
            #     .filter(rank__gte=0.4).order_by('-rank')

            # search with search trigram similarity
            result1 = Post.published.annotate(
                similar=TrigramSimilarity('title', query)).filter(similar__gt=0.1)

            result2 = Post.published.annotate(
                similar=TrigramSimilarity('description', query)).filter(similar__gt=0.1)

            result3 = Post.published.annotate(
                similar=TrigramSimilarity('images__description', query)).filter(similar__gt=0.05)
            results = (result1 | result2 | result3).order_by('-similar').annotate(
                headline=SearchHeadline("description", query))

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)


def profile(request):
    user = request.user
    posts = Post.published.filter(auther=user)
    context = {
        "posts": posts
    }
    return render(request, 'blog/profile.html', context)
