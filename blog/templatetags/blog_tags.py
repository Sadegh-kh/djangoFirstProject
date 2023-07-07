from django import template
from ..models import Post, Comment

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag(name="all_comment")
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag(name="last_published")
def last_date():
    return Post.published.last().publish.strftime("%Y/%m/%d-%H:%M")


@register.inclusion_tag("partials/latest_posts_tag.html")
def latest_post(count=4):
    last_posts = Post.published.order_by("-publish")[:count]
    context = {
        "last_posts": last_posts
    }
    return context
