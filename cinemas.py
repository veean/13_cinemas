from bs4 import BeautifulSoup
import requests
import argparse
import random
import time


NOT_ARTHOUSE = 15
PROXY_FABRIC = 'http://www.freeproxy-list.ru/api/proxy'
DEFAULT_TOP_MOVIES_NUMBER = 10


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


def fetch_movie_info(movie_title, proxy_list, delay_to_next_request=20, time_to_wait_response=10):

    movie_url_mask = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query='
    headers = {'Accept': 'text/plain',
               'Accept-Encoding': 'UTF-8',
               'Accept-Language': 'Ru-ru',
               'Content-Type': 'text/html;charset=UTF-8',
               'User-Agent': 'Agent:Mozilla/5.0 (Windows NT 6.1; WOW64)'}

    try:
        kinopoisk_response = requests.get('{}{}'.format(movie_url_mask, movie_title),
                                          proxies={"http": random.choice(proxy_list)},
                                          headers=headers, timeout=time_to_wait_response).content
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
        return None

    movie_soup = BeautifulSoup(kinopoisk_response, 'html.parser')
    raw_movie_rate = movie_soup.find('span', class_='rating_ball')
    raw_movie_voters = movie_soup.find('span', class_='ratingCount')
    movie_rate = float(raw_movie_rate.text) if raw_movie_rate else 0
    movie_voters = raw_movie_voters.text if raw_movie_voters else 0

    time.sleep(delay_to_next_request)
    movie_info = {'title': movie_title,
                  'rate': movie_rate,
                  'votes': movie_voters
                  }

    return movie_info


def get_proxy_to_avoid_ban(url):
    params_for_proxies_list = {'anonymity': 'true', 'token': 'demo'}
    proxies_list = requests.get(url, params=params_for_proxies_list).text.splitlines()
    return proxies_list


def output_movies_to_console(movies, top_number=DEFAULT_TOP_MOVIES_NUMBER):
    sorted_movies = sorted(movies, key=lambda movie: movie['rate'], reverse=True)[:top_number]
    output_template = '{}.Movie {title} has rating : {rate} with {votes} votes'
    for position, movie_info in enumerate(sorted_movies, 1):
        print(output_template.format(position, **movie_info))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--top', type=int, help='specify a number of top films to print')
    top_movies_number = parser.parse_args().top

    movies_list = parse_afisha_list(fetch_afisha_page())
    proxies_list = get_proxy_to_avoid_ban(PROXY_FABRIC)

    wanted_movie_info = [fetch_movie_info(movie['movie_title'], proxies_list) for movie in movies_list]

    if top_movies_number:
        print('Collecting TOP {} rated movies ...'.format(top_movies_number))
        output_movies_to_console(wanted_movie_info, top_movies_number)
    else:
        print('Collecting TOP {} rated movies ...'.format(DEFAULT_TOP_MOVIES_NUMBER))
        output_movies_to_console(wanted_movie_info)
