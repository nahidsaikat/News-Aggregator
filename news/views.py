import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import HeadLine


def scrape(request):
    session = requests.Session()
    session.headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
    url = 'https://www.theonion.com/'

    content = session.get(url, verify=False).content
    soup = BSoup(content, 'html.parser')
    news = soup.find_all('div', {'class': 'curation-module__item'})

    for article in news:
        main = article.find_all('a')[0]
        link = main['href']
        image_src = str(main.find('img')['arcset']).split(' ')[-4]
        title = main['title']

        headline = HeadLine()
        headline.title = title
        headline.url = link
        headline.image = image_src
        headline.save()
    return redirect('../')


def news_list(request):
    headlines = HeadLine.objects.all()[::-1]
    context = {
        'object_list': headlines
    }
    render(request, 'news/home.html', context)
