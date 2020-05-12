# News-Aggregator

### Dependencies
* Python == 3.8
* Django == 3.0.5
* beautifulsoup4 == 4.9.0
* requests == 2.23.0

### Setup Instructions
* git clone https://github.com/nahidsaikat/NewsAggregator.git
* cd NewsAggregator
* pipenv install
* pipenv shell
* python manage.py migrate
* python manage.py loaddata news_provider.json
* python manage.py runserver

### Features
* Grab THE ONION news
* Grab BBC NEWS
* Search by title
* Pagination
* Mark read
* Mark unread

### Screen Shots
* Home Page Top 
![Image description](https://raw.githubusercontent.com/nahidsaikat/NewsAggregator/master/docs/images/1.jpg)

* Home Page Bottom
![Image description](https://raw.githubusercontent.com/nahidsaikat/NewsAggregator/master/docs/images/2.jpg)
