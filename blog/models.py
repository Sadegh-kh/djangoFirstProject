from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ("DR", "Draft")
        PUBLISH = ("PB", "Publish")
        REJECT = ("RJ", "Reject")

    CATEGORY_CHOICES = (
        ('هوش مصنوعی', 'هوش مصنوعی'),
        ('بلاکچین', 'بلاکچین'),
        ('زبان برنامه نویسی', 'زبان برنامه نویسی'),
        ('سایر', 'سایر'),
    )
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
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='سایر', verbose_name='دسته بندی')

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

    def save(self, *args, **kwargs):
        # method 1 for autofill slug field
        self.slug = slugify(self.title + " " + str(self.auther.id))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        images = self.images.all()
        for image in images:
            # storage is django backend storage (media/) and path is exact location of file
            storage, path = image.image_file.storage, image.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")

    # char field instead of integer field because we don't want to calculate
    phone = models.CharField(max_length=12, verbose_name="شماره موبایل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")

    send_time = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ارسال", null=True)


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


def upload_to(instance, filename):
    datetime = timezone.now()
    return f"post_images/{datetime.strftime('%Y')}/{datetime.strftime('%m')}/{instance.post.auther.username}/{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name='پست')
    image_file = ResizedImageField(verbose_name='عکس', upload_to=upload_to, size=[300, 300], quality=75)
    title = models.CharField(verbose_name='موضوع', max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        image_name = self.image_file.name.split("/")[-1]
        return self.title if self.title else image_name

    def delete(self, *args, **kwargs):
        image = self.image_file
        storage, path = image.storage, image.path
        storage.delete(path)
        super().delete(*args, **kwargs)


# method 1 for delete image from media root
# @receiver(post_delete, sender=Image)
# def delete_image(sender, instance, **kwargs):
#     """ delete old image from media root when deleted database """
#     instance.image_file.delete(save=False)
#

@receiver(pre_save, sender=Image)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image_file.path
        storage = instance.image_file.storage
        try:
            new_img = instance.image_file.path
        except:
            new_img = None
        if new_img != old_img and storage.exists(old_img):
            storage.delete(old_img)
    except:
        pass
