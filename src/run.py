from pprint import pprint

from src.web_scrapping.habr import get_post_by_keywords


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

parsed_data = get_post_by_keywords(KEYWORDS, True)

if __name__ == '__main__':
    pprint(parsed_data)
