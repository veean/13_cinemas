import requests
from bs4 import BeautifulSoup
import time
import random


NOT_ARTHOUSE = 15


def fetch_afisha_page():
    movie_info = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    return movie_info.content


def extract_casual_movies(movies_list):
    casual_films = [film for film in movies_list if film['cinemas_count'] > NOT_ARTHOUSE]
    return casual_films


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    raw_movies_info = soup.find_all('div', {'class': 'object s-votes-hover-area collapsed'})
    movies_info_list = []

    for movie in raw_movies_info:
        movie = {'movie_title': movie.find('h3', class_='usetags').text, 'cinemas_count': len(movie.find('tbody'))}
        movies_info_list.append(movie)

    return extract_casual_movies(movies_info_list)


def fetch_movie_info(movie_title):
    movie_url_mask = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query='
    user_agent = {'Accept': 'text/plain',
                  'Accept-Encoding': 'UTF-8',
                  'Accept-Language': 'Ru-ru',
                  'Content-Type': 'text/html;charset=UTF-8',
                  'User-Agent': 'Agent:Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    kinopoisk_response = requests.get('{}{}'.format(movie_url_mask, movie_title), headers=user_agent).content
    movie_soup = BeautifulSoup(kinopoisk_response, 'html.parser')
    movie_rate = movie_soup.find('span', class_='rating_ball').text
    movie_voters = movie_soup.find('span', class_='ratingCount').text
    return movie_rate, movie_voters


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    films = parse_afisha_list(fetch_afisha_page())
    for movie_info in films:
        rate, votes = fetch_movie_info(movie_info['movie_title'])
        time.sleep(random.randrange(10, 34))
        print('{} rating : {} votes amount : {}'.format(movie_info['movie_title'], rate, votes))



