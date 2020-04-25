from django.contrib import admin
from news.models import HeadLine, NewsProvider


admin.site.register(HeadLine)
admin.site.register(NewsProvider)
