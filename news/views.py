from django.shortcuts import render, redirect, reverse

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
    button_text = 'Grab All News'
    provider_code = request.GET.get('provider_code', None)
    headlines = HeadLine.objects.all()

    if provider_code:
        provider = NewsProvider.objects.filter(code=provider_code).first()
        button_text = 'Grab ' + provider.get_code_display()
        if provider:
            headlines = headlines.filter(provider=provider)
    headlines = headlines.order_by("-pk")

    context = {
        'object_list': headlines,
        'button_text': button_text.upper(),
        'provider_code': provider_code or ''
    }
    return render(request, 'news/home.html', context)


def mark_read(request, pk, **kwargs):
    headline = HeadLine.objects.filter(pk=pk).first()
    if headline:
        headline.is_read = request.GET.get('mark', False)
        headline.save()
    return redirect('home')
