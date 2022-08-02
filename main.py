import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'вода', 'лет']


def get_html(link):
    HEADERS = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
    respounse = requests.get(link, headers=HEADERS)
    text = respounse.text
    return text


def main():
    html = get_html('https://habr.com/ru/all/')
    parse_habr(html, tags=KEYWORDS)


def get_patern(list):
    patern = '\\W('
    for i in range(len(list)):
        if i != 0 and i != len(list)-1:
            patern += f'|{list[i].lower()}'
        if i == len(list)-1:
            patern += f'|{list[i].lower()})\\W'
        if i == 0:
            patern += f'{list[i].lower()}'
    return patern


def parse_habr(html, tags=[]):
    patern = get_patern(tags)
    soup = BeautifulSoup(html, features='html.parser')
    articles = soup.find_all('div', class_='tm-article-snippet')
    for article in articles:
        article_title = article.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').text
        article_time = article.find('span', class_='tm-article-snippet__datetime-published').text
        article_href = article.find('a', class_='tm-article-snippet__title-link')['href']
        href = 'https://habr.com' + article_href
        regex_output = re.findall(patern, article_title.lower())
        if len(regex_output) > 0:
            print(f'{article_time} - {article_title} - {href}')
            print()
            _parse_web_in_parse(href)


def _parse_web_in_parse(link):
    html = get_html(link)
    soup = BeautifulSoup(html, features='html.parser')
    parse_text(soup)


def parse_text(soup):
    p = soup.find_all('p')
    get_word(KEYWORDS, p)


# функция вернет кол-во использований слов из KEYWORDS
def get_word(KEYWORDS, text):
    find_list = []
    patern = get_patern(KEYWORDS)
    for _text in text:
        _text = _text.text
        find_list.append(re.findall(patern, _text))
    elem= []
    for el in find_list:
        for _el in el:
            elem.append(_el)
    key_dict = {}
    for key in KEYWORDS:
        print(f'Слово {key} встречается {elem.count(key)} раз/a')


def asd():
    pass




if __name__ == '__main__':
    main()
