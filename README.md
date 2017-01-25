# Cinemas

Данный скрипт берет [отсюда](http://www.afisha.ru/msk/schedule_cinema/) фильмы идущие в кинотеатрах, затем собирает о фильмах информацию на [кинопоиске](https://www.kinopoisk.ru/)
и выводит ТОП (10 по умолчанию) фильмов с самым большим рейтингом.

## Скачивание скрипта и зависимостей
 
     git clone https://github.com/veean/13_cinemas.git
     cd 13_cinemas
     pip3 install -r requirements.txt
     
## Запуск скрипта

* Запуск скрипта осуществляется командой `python cinemas.py `   
* Параметром `-t [top number]` можно передать количество топовых фильмов
неартхаусных фильмов, идущих на данный момент в кино (по умолчанию выводит 10 штук).

## Вывод скрипта
    $python cinemas.py
    Collecting TOP 10 rated movies ...
    1.Movie Ла-Ла Ленд has rating : 8.557 with 39 383 votes
    2.Movie Невеста has rating : 7.664 with 4076 votes
    3.Movie Изгой-один: Звездные войны. Истории has rating : 7.502 with 42 798 votes
    4.Movie По Млечному Пути has rating : 7.166 with 1081 votes
    5.Movie Пассажиры has rating : 7.154 with 43 789 votes
    6.Movie Рай has rating : 7.137 with 1244 votes
    7.Movie Преисподняя has rating : 7.045 with 588 votes
    8.Movie Почему он? has rating : 6.817 with 9141 votes
    9.Movie Закон ночи has rating : 6.73 with 5573 votes
    10.Movie Иллюзия любви has rating : 6.655 with 311 votes


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
