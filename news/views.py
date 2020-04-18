import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import HeadLine


def get_session():
    session = requests.Session()
    session.headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
    return session


def get_content(url):
    session = get_session()
    content = session.get(url, verify=False).content
    return content


def scrape(request):
    url = 'https://www.theonion.com/'
    content = get_content(url)
    soup = BSoup(content, 'html.parser')
    article_list = soup.find_all('article')

    for article in article_list:
        try:
            image = ''
            h4 = article.find_all('h4')[0]
            img = article.find_all('img')
            if len(img) > 0:
                img = img[0]
                if img.has_attr('data-srcset'):
                    image = str(img['data-srcset']).split(' ')[4]
                elif img.has_attr('srcset'):
                    image = str(img['srcset']).split(' ')[4]
            url = article.find_all('a')[-1]['href']

            if not HeadLine.objects.filter(url=url).exists():
                headline = HeadLine()
                headline.title = h4.text
                headline.url = url
                headline.image = image
                headline.save()
        except Exception as ex:
            print(ex)

    return redirect('../')


def news_list(request):
    headlines = HeadLine.objects.all()[::-1]
    context = {
        'object_list': headlines
    }
    return render(request, 'news/home.html', context)
