from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")

    # choice field
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")

    objects = models.Manager()
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
