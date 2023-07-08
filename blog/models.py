from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ("DR", "Draft")
        PUBLISH = ("PB", "Publish")
        REJECT = ("RJ", "Reject")

    # relation
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posted", verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=250, verbose_name="موضوع")
    description = models.TextField(verbose_name="توضیحات")

    slug = models.SlugField(max_length=250, verbose_name="سلاگ")

    # date fields
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")

    # choice field
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")

    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")

    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=["-publish"])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_item", args=[self.id])


class Ticket(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")

    # char field instead of integer field because we don't want to calculate
    phone = models.CharField(max_length=12, verbose_name="شماره موبایل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")


class Comment(models.Model):
    # post.comments/ post.comments.all() / comment.post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=255, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    update = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت پذیرش")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created', 'name'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name} : {self.post}"
