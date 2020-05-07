from django.urls import path
from news.views import scrape, news_list, mark_read, search, provider_home

urlpatterns = [
  path('search/', search, name="search"),
  path('scrape/', scrape, name="scrape"),
  path('mark_read/<int:pk>/', mark_read, name="mark_read"),
  path('provider/<int:code>/', provider_home, name="provider_home"),
  path('', news_list, name="home"),
]
