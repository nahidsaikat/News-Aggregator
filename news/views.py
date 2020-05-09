from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from news.models import HeadLine, NewsProvider
from news.scraper import BaseScraper


def scrape(request):
    provider_code = request.GET.get('provider_code', None)
    if provider_code:
        scraper = None
        for ChildClass in BaseScraper.__subclasses__():
            if ChildClass.provider_code.value == int(provider_code):
                scraper = ChildClass()
                break
        if scraper:
            scraper.scrape()
    else:
        for ChildClass in BaseScraper.__subclasses__():
            scraper = ChildClass()
            scraper.scrape()

    return redirect(reverse('home') + f'?provider_code={provider_code}')


def news_list(request):
    return get_news_list_response(request)


def provider_home(request, code, **kwargs):
    return get_news_list_response(request, provider_code=code)


def get_news_list_response(request, search_title='', provider_code=None):
    button_text = 'Grab All News'
    provider_code = provider_code or request.GET.get('provider_code', None)
    headlines = HeadLine.objects.all()

    if search_title:
        headlines = headlines.filter(title__icontains=search_title)

    if provider_code:
        provider = NewsProvider.objects.filter(code=provider_code).first()
        button_text = 'Grab ' + provider.get_code_display()
        if provider:
            headlines = headlines.filter(provider=provider)

    headlines = headlines.order_by("-pk")

    page_no = request.GET.get('page', 1)
    paginator = Paginator(headlines, 20)
    try:
        headlines = paginator.page(page_no)
    except PageNotAnInteger:
        headlines = paginator.page(1)
    except EmptyPage:
        headlines = paginator.page(paginator.num_pages)

    context = {
        'object_list': headlines,
        'button_text': button_text.upper(),
        'provider_code': provider_code or '',
        'page_no': page_no,
    }
    return render(request, 'news/home.html', context)


def mark_read(request, pk, **kwargs):
    page_no = request.GET.get('page', 1)
    headline = HeadLine.objects.filter(pk=pk).first()
    if headline:
        headline.is_read = request.GET.get('mark', False)
        headline.save()

    url_name = 'home'
    url_args = []
    provider_code = request.GET.get('provider_code', False)
    if provider_code:
        url_name = 'provider_home'
        url_args = [provider_code]

    url = f'{reverse(url_name, args=url_args)}?page={page_no}'

    return redirect(url)


def search(request, **kwargs):
    return get_news_list_response(request, search_title=request.POST.get('search', ''))
