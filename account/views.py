from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# manual login user (fbv)
# def user_login(request):
#     if request.method == "POST":
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     return HttpResponse('user is not active')
#             else:
#                 return HttpResponse('user not found')
#
#     else:
#         form = forms.LoginForm()
#     return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register_view(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            models.Account.objects.create(user=user)
            login(request, user)
            return redirect('blog:profile')
    else:
        form = forms.UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


@login_required
def edit_account(request):
    account = get_object_or_404(models.Account, user=request.user)
    if request.method == 'POST':
        form_user = forms.UserEditForm(request.POST, instance=request.user)
        form_account = forms.AccountEditForm(request.POST, request.FILES, instance=account)
        if form_user.is_valid() and form_account.is_valid():
            form_user.save()
            form_account.save()
            return redirect('blog:profile')
    else:
        form_user = forms.UserEditForm(instance=request.user)
        form_account = forms.AccountEditForm(instance=account)

    context = {
        "form_user": form_user,
        "form_account": form_account
    }

    return render(request, 'account/forms/edit_account.html', context)


@login_required
def profile(request):
    posts = Post.published.filter(auther=request.user)
    paginator = Paginator(posts, 4)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        "posts": posts
    }
    return render(request, 'account/profile.html', context)


def profile_comments(request, pk):
    post = get_object_or_404(Post, id=pk)
    context = {
        'post': post
    }
    return render(request, 'account/profile_comments.html', context)


def author_detail(request, author):
    user = User.objects.get(username=author)
    account = models.Account.objects.get(user=user)
    posts = Post.published.filter(auther=user)
    context = {
        'user': user,
        'account': account,
        'posts': posts
    }
    return render(request, 'account/author.html', context)
