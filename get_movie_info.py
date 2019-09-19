import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import asyncio
from multiprocessing import Pool
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1



headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

movie_list = db.naver_movie_list.find({}, {'_id': False})
docs = []
for movie in movie_list:
    data = requests.get('https://movie.naver.com/' + movie['href'], headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    movie_genre = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a')
    genre_list = []
    for genre in movie_genre:
        genre_list.append(genre.text)
    movie_dir = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a')
    dir_list = []
    for dir in movie_dir:
        dir_list.append(dir.text)
    actr = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p > a')
    act_list = []
    for act_name in actr:
        act_list.append(act_name.text)
    doc = {'title':movie['title'], 'href':movie['href'], 'genre':genre_list, 'director':dir_list, 'actor':act_list}
    docs.append(doc)
db.movie_info.insert_many(docs)

