import requests
from bs4 import BeautifulSoup as BSoup

from news.models import HeadLine, NewsProvider


class BaseScraper(object):
    provider_code = None

    def __init__(self):
        if not self.provider_code:
            raise Exception('You must define a provider_code')
        self.provider = NewsProvider.objects.filter(code=self.provider_code).get()

    @staticmethod
    def get_session():
        session = requests.Session()
        session.headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
        return session

    def get_content(self, url=''):
        session = self.get_session()
        content = session.get(url or self.provider.url, verify=False).content
        return content

    def get_soup_obj(self, url=''):
        content = self.get_content(url=url)
        soup = BSoup(content, 'html.parser')
        return soup

    def scrape(self):
        raise NotImplementedError('<scrape> method should be implemented')

    @staticmethod
    def create_headline(**kwargs):
        headline = None
        if not HeadLine.objects.filter(url=kwargs.get('url')).exists():
            headline = HeadLine(**kwargs)
            headline.save()
        return headline


class TheOnionScraper(BaseScraper):
    provider_code = NewsProvider.ProviderCode.THE_ONION

    def scrape(self):
        soup = self.get_soup_obj()
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

                self.create_headline(**{
                    'provider': self.provider,
                    'title': h4.text,
                    'url': url,
                    'image': image,
                    'published_at': ''  # self.get_published_at(url) # This method call slow down the scraping.
                })
            except Exception as ex:
                print(ex)

        return {'status': 'success', 'message': 'Scraped Successfully.'}

    def get_published_at(self, url):
        try:
            soup = self.get_soup_obj(url)
            article_div = soup.find_all('div', {'class': 'js_starterpost'})[0]
            time = article_div.find_all('time')[0].text
        except Exception as ex:
            print(ex)
            time = ''

        return time


class BBCNewsScraper(BaseScraper):
    provider_code = NewsProvider.ProviderCode.BBC_NEWS

    def scrape(self):
        soup = self.get_soup_obj()

        # Most Watch
        li_list = soup.find('ol', {'class': 'gel-layout'}).find_all('li')
        for li in li_list:
            try:
                link = li.find('a')
                url = self.provider.url.rpartition('/')[0] + link['href']
                self.create_headline(**{
                    'provider': self.provider,
                    'title': link.find_all('span')[-1].get_text(),
                    'url': url,
                    'image': '',
                    'published_at': ''
                })
            except Exception as ex:
                print(ex)

        # Most Read
        li_list = soup.find('div', {'class': 'nw-c-most-read__items'}).find('ol', {'class': 'gel-layout__item'}).find_all('li')
        for li in li_list:
            try:
                link = li.find('a')
                url = self.provider.url.rpartition('/')[0] + link['href']
                self.create_headline(**{
                    'provider': self.provider,
                    'title': link.get_text(),
                    'url': url,
                    'image': '',
                    'published_at': ''
                })
            except Exception as ex:
                print(ex)

        # Main Articles
        div_list = soup.find_all('div', {'class': 'gel-layout__item'})
        for div in div_list:
            img = div.find('img')
            link = div.find('a')
            if img and link:
                try:
                    url = self.provider.url.rpartition('/')[0] + link['href']
                    if img.has_attr('srcset'):
                        image = img['srcset'].split(' ')[-2]
                    else:
                        image = img['data-src'].format(width=820)

                    self.create_headline(**{
                        'provider': self.provider,
                        'title': link.get_text(),
                        'url': url,
                        'image': image,
                        'published_at': ''
                    })
                except Exception as e:
                    print(e)
