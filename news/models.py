from django.db import models


class NewsProvider(models.Model):
    class Code(models.IntegerChoices):
        THE_ONION = 1
        BBC_NEWS = 2

    title = models.CharField(max_length=200)
    url = models.TextField()
    code = models.IntegerField(choices=Code.choices)

    def __str__(self):
        return self.title


class HeadLine(models.Model):
    provider = models.ForeignKey(NewsProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    url = models.TextField()
    published_at = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
