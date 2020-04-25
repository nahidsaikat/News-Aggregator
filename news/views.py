from django.shortcuts import render, redirect

from news.models import HeadLine, NewsProvider
from news.scraper import TheOnionScraper


def scrape(request):
    provider = NewsProvider.objects.filter(code=NewsProvider.Code.THE_ONION).get()
    scraper = TheOnionScraper(provider=provider)
    scraper.scrape()
    return redirect('../')


def news_list(request):
    headlines = HeadLine.objects.all()[::-1]
    context = {
        'object_list': headlines
    }
    return render(request, 'news/home.html', context)
