import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1                      # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
docs = []
temp_lists = []

for page_num in range(1,6):

    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190827&page='+str(page_num),headers=headers)
    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    # select : 여러개 select_on : 한개
    tr_result = soup.select('#old_content > table > tbody > tr > td.title > div > a')

    for movie in tr_result:
        movie_title = {}
        doc = {'title':movie.text, 'href':movie['href']}
        # movie_title.append(movie.text)
        movie_title['title'] = movie.text
        movie_title['href'] = movie['href']
        data = requests.get('https://movie.naver.com/' + movie['href'], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        tr_user_number = soup.select(
            '#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_total > strong > em')
        for number in tr_user_number:
            str1 = number.text.strip()
            usernum_str = str1.replace(',', '')
            usernum = int(usernum_str)
            user_num_page = int(usernum / 10);
            if usernum % 10 != 0:
                user_num_page += 1
        doc['page'] = user_num_page
        movie_title['pages'] = user_num_page
        temp_lists.append(movie_title)

        docs.append(doc)

db.naver_movie_list.insert_many(docs)
dics_temp = {'list':temp_lists}
db.easy_movie_list.insert_one(dics_temp)

