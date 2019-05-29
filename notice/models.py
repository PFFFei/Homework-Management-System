from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=50)
    body = RichTextUploadingField()
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notice:detail',args=[str(self.pk)])

    class Meta:
	    verbose_name='通知'
	    verbose_name_plural = verbose_name
