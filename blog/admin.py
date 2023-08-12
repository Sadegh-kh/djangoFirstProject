from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

admin.AdminSite.site_header = 'پنل مدیریت جنگو'
admin.AdminSite.site_title = "جنگو"
admin.AdminSite.index_title = "پنل مدیریت"


# Inline Admin
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "auther", "publish", 'category', "status"]
    list_display_links = ['auther', 'title']
    list_filter = [("publish", JDateFieldListFilter), 'status', 'auther']
    search_fields = ['title', 'description','category']
    list_editable = ['status','category']
    prepopulated_fields = {'slug': ['auther', 'title']}
    raw_id_fields = ('auther',)
    date_hierarchy = 'publish'
    ordering = ['-publish', 'title']
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "phone", 'send_time']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = [('created', JDateFieldListFilter), ('update', JDateFieldListFilter), 'active']
    list_editable = ['active']
    search_fields = ['post', 'name', 'body']
    ordering = ['created']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']
