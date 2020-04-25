# News-Aggregator

### Dependencies
>Python == 3.8
>
>Django == 3.0.5
>
>beautifulsoup4 == 4.9.0
>
>requests == 2.23.0

### Setup Instructions
* git clone https://github.com/nahidsaikat/NewsAggregator.git
* cd NewsAggregator
* pipenv install
* pipenv shell
* python manage.py migrate
* python manage.py loaddata news_provider.json
* python manage.py runserver
