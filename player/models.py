from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Music(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/images/')
    music = models.FileField(upload_to='uploads/music')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
