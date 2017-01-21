import requests
from bs4 import BeautifulSoup

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
        movie_ = {'movie_title': movie.find('h3', class_='usetags').text, 'cinemas_count': len(movie.find('tbody'))}
        movies_info_list.append(movie)

    return extract_casual_movies(movies_info_list)


def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    pass
