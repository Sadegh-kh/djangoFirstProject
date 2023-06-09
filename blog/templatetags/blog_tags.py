from django import template
from ..models import Post, Comment
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

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


@register.simple_tag
def most_comments(count):
    return Post.published.annotate(comment_count=Count("comments")).order_by("-comment_count")[:count]


@register.inclusion_tag("partials/latest_posts_tag.html")
def latest_post(count=4):
    last_posts = Post.published.order_by("-publish")[:count]
    context = {
        "last_posts": last_posts
    }
    return context


# filters
@register.filter("markdown")
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter
def censorship(text: str):
    blasphemes = ['fuck', 'عوضی', 'گوه', 'کثافت', 'bitch']
    for i in blasphemes:
        if text.find(i):
            text=text.replace(i, "*****")

    return mark_safe(text)
