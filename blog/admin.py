from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "auther", "publish", "status"]
    list_display_links = ['auther', 'title']
    list_filter = ["publish", 'status', 'auther']
    search_fields = ['title', 'description', 'auther']
    list_editable = ['status']
    prepopulated_fields = {'slug': ['auther', 'title']}
    raw_id_fields = ('auther',)
    date_hierarchy = 'publish'
    ordering = ['-publish', 'title']
