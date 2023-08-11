from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField


# Create your models here.
def upload_to(instance, filename):
    return f"avatar/{instance.user.username}/{filename}"


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(blank=True, null=True, verbose_name='بایو')
    photo = ResizedImageField(verbose_name='عکس', upload_to=upload_to, size=[500, 500], quality=60, null=True,
                              blank=True)
    job = models.CharField(max_length=255, verbose_name='شغل', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'

    def delete(self, *args, **kwargs):
        photo = self.photo
        storage, path = photo.storage, photo.path
        storage.delete(path)
        super().delete(*args, **kwargs)
