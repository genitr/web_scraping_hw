"""Функции для парсинга статей с сайта https://habr.com"""

import requests as request
from fake_headers import Headers
import bs4


headers = Headers(browser='chrome', os='win').generate()

HABR_BASE_URL = 'https://habr.com'
HABR_ARTICLE_URL = HABR_BASE_URL + '/ru/articles/'


def get_post_by_keywords(keywords: list[str], only_in_title=False) -> list[str]:
    """
    Функция ищет опубликованные статьи по ключевым словам.
    Поиск осуществляется как по заголовку, так и по содержимому статьи.
    :param keywords: Список ключевых слов
    :param only_in_title: Если установлено на True, то поиск осуществляется
    только по заголовку статьи
    :return: Список статей
    """
    response = request.get(HABR_ARTICLE_URL, headers=headers)
    soup = bs4.BeautifulSoup(response.text, features='lxml')

    post_list = soup.select_one('div.tm-articles-subpage')
    article_list = post_list.select('article.tm-articles-list__item')

    parsed_data = []

    for article in article_list:
        date = article.select_one('time')['title']
        title = article.select_one('h2.tm-title').select_one('span').text
        link = HABR_BASE_URL + article.select_one('a.tm-title__link')['href']

        title_lower = title.lower()

        # Ищем совпадение в заголовке статьи
        if any([key in title_lower for key in keywords]):
            parsed_data.append(f'<{date}>-<{title}>-<{link}>')
        # Иначе ищем во всей статье
        else:
            if not only_in_title:
                post_page = request.get(link, headers=headers)
                soup_page = bs4.BeautifulSoup(post_page.text, features='lxml')

                post_text = soup_page.select_one('div.tm-article-body').text.lower()

                if any([key in post_text for key in keywords]):
                    parsed_data.append(f'<{date}>-<{title}>-<{link}>')

    if len(parsed_data) == 0:
        return f'Извините, по ключевым словам {keywords} ничего не найдено.'

    return parsed_data


if __name__ == '__main__':
    print()