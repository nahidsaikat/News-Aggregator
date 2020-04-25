from django.contrib import admin
from news.models import HeadLine, NewsProvider


class NewsProviderAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'code')


admin.site.register(HeadLine)
admin.site.register(NewsProvider, NewsProviderAdmin)
