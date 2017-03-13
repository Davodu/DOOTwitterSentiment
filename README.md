## Overview
A Django App which crawls live tweets and creates a pie chart to compare the sentiments associated with two words(or phrases) 

## Technology Stack
- [Django](https://www.djangoproject.com/) (Server)
- [Google charts](https://developers.google.com/chart/interactive/docs/reference) 
- [Twitter Bootstrap](http://getbootstrap.com/)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)(Natural Language Processing)

## Getting Started
Clone the repo:
```sh
git clone https://github.com/Davodu/DOOTwitterSentiment.git
cd DOOTwitterSentiment
```
Install all dependencies from package.txt file
```sh
pip install -r package.txt
```
Fill in details of ```py secret.py```

## Run

```sh
python manage.py runserver
```
To increase accuracy, modify ``` Num_tweets``` variable in  main_app/analyze.py

## Reference & Other resources
- [Django](https://www.djangoproject.com/ ) <br>
- [Google charts](https://developers.google.com/chart/interactive/docs/reference)

## Live app [here](http://davodu.pythonanywhere.com/main_app/home/) 
