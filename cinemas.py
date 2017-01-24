import requests
from bs4 import BeautifulSoup
import time
import random


NOT_ARTHOUSE = 15
PROXY_URL = 'http://www.freeproxy-list.ru/api/proxy'


def fetch_afisha_page():
    movie_info = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    return movie_info.content


def extract_casual_movies(movies_list):
    casual_movies = [movie for movie in movies_list if movie['cinemas_count'] > NOT_ARTHOUSE]
    return casual_movies


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    raw_movies_info = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    movies_info_list = []

    for movie in raw_movies_info:
        movie = {'movie_title': movie.find('h3', class_='usetags').text, 'cinemas_count': len(movie.find('tbody'))}
        movies_info_list.append(movie)

    return extract_casual_movies(movies_info_list)


def fetch_movie_info(movie_title, proxy_list):
    movie_url_mask = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query='
    headers = {'Accept': 'text/plain',
               'Accept-Encoding': 'UTF-8',
               'Accept-Language': 'Ru-ru',
               'Content-Type': 'text/html;charset=UTF-8',
               'User-Agent': 'Agent:Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    time_to_wait_response = 10

    try:
        kinopoisk_response = requests.get('{}{}'.format(movie_url_mask, movie_title),
                                          proxy={"http": random.choice(proxy_list)},
                                          headers=headers, timeout=time_to_wait_response).content
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
        return None

    movie_soup = BeautifulSoup(kinopoisk_response, 'html.parser')
    movie_rate = movie_soup.find('span', class_='rating_ball').text
    movie_voters = movie_soup.find('span', class_='ratingCount').text
    return movie_title, movie_rate, movie_voters


def proxy_to_avoid_ban(url):
    params_for_proxies_list = {'anonymity': 'true', 'token': 'demo'}
    proxies_list = requests.get(url, params=params_for_proxies_list).text.splitlines()
    return proxies_list


def output_movies_to_console(movies, top_number):
    sorted_movies = sorted(movies, key=lambda movie: movie[1], reverse=True)[:top_number]
    for position, movie_info in enumerate(sorted_movies):
        print('{}.Movie {} has rating : {} with {} votes'.format(position, movie_info[0], movie_info[1], movie_info[2]))


if __name__ == '__main__':
    films = parse_afisha_list(fetch_afisha_page())

    # for movie_info in films:
    #     rate, votes = fetch_movie_info(movie_info['movie_title'])
    #     time.sleep(random.randrange(10, 34))
    #     print('{} rating : {} votes amount : {}'.format(movie_info['movie_title'], rate, votes))



