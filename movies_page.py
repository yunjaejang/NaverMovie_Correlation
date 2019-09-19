import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

movie_list = db.naver_movie_list.find({},{'_id':False})
update_lists = []
data_json = {}

for x in movie_list:
    print(x['title'], x['href'])
    data_json[x['title']] = []
    update_one = {}
    data = requests.get('https://movie.naver.com/' + x['href'], headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    tr_image = soup.select('#content > div.article > div.mv_info_area > div.poster > a > img')
    temp_list = db.movie_info.find_one({'title': x['title'], 'href':x['href']}, {'_id': False})
    update_one = temp_list.copy()

    update_one['href'] = x['href']
    update_one['src'] = tr_image[0]['src']

    data_json[x['title']].append(update_one)

with open('movie_info.json', 'w', encoding='UTF-8') as outfile:
    json.dump(data_json, outfile, ensure_ascii=False, indent=4)


#     update_lists.append(update_one)
# db.movie_info_update.insert_many(update_lists)