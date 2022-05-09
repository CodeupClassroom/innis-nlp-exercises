import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_blog_article_urls():
    headers = {'user-agent': 'Innis Codeup Data Science'}
    response = requests.get('https://codeup.com/blog/', headers=headers)
    soup = BeautifulSoup(response.text)
    urls = [a.attrs['href'] for a in soup.select('a.more-link')]
    return urls

def parse_blog_article(soup):
    return {
        'title': soup.select_one('h1.entry-title').text,
        'published': soup.select_one('.published').text,
        'content': soup.select_one('.entry-content').text.strip(),
    }

def get_blog_articles(use_cache=True):
    if os.path.exists('codeup_blog_articles.json') and use_cache:
        return pd.read_json('codeup_blog_articles.json')

    urls = get_blog_article_urls()
    articles = []

    for url in urls:
        print(f'fetching {url}')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)
        articles.append(parse_blog_article(soup))

    df = pd.DataFrame(articles)
    df.to_json('codeup_blog_articles.json', orient='records')
    return df

def parse_news_card(card, category):
    output = {}

    output['category'] = category
    output['title'] = card.select_one('a.clickable').text.strip()

    card_content = card.select_one('.news-card-content')
    output['content'] = card_content.select_one('div').text

    author_and_time = card_content.select_one('.news-card-author-time')
    output['author'] = author_and_time.select_one('.author').text
    output['published'] = author_and_time.select_one('.time').attrs['content']

    return output

def parse_news_category(category):
    url = 'https://inshorts.com/en/read/' + category
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    cards = soup.select('.news-card')
    articles = []

    for card in cards:
        articles.append(parse_news_card(card, category))

    return articles

def get_news_articles(use_cache=True):
    if os.path.exists('news_articles.json') and use_cache:
        return pd.read_json('news_articles.json')

    categories = ['business', 'sports', 'technology', 'entertainment']

    articles = []

    for category in categories:
        print(f'Getting {category} articles')
        articles.extend(parse_news_category(category))

    df = pd.DataFrame(articles)
    df.to_json('news_articles.json', orient='records')
    return df
