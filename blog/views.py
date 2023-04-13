from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index_page(request):
    return HttpResponse("index page")


def post_list(request):
    return HttpResponse("list of posts")


def post_item(request, id):
    return HttpResponse(f"post : {id}")
