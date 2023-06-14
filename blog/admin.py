from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

admin.AdminSite.site_header = 'پنل مدیریت جنگو'
admin.AdminSite.site_title = "جنگو"
admin.AdminSite.index_title = "پنل مدیریت"


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "auther", "publish", "status"]
    list_display_links = ['auther', 'title']
    list_filter = [("publish", JDateFieldListFilter), 'status', 'auther']
    search_fields = ['title', 'description', 'auther']
    list_editable = ['status']
    prepopulated_fields = {'slug': ['auther', 'title']}
    raw_id_fields = ('auther',)
    date_hierarchy = 'publish'
    ordering = ['-publish', 'title']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "phone"]
