import requests
from bs4 import BeautifulSoup
import asyncio
from multiprocessing import Pool
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

def user_get(movie):
    mt = movie['title']
    print("{} 시작".format(mt))
    npages = int(movie['pages'])
    new_str = movie['href']
    code_str = new_str.replace('/movie/bi/mi/basic.nhn?code=', '')

    docs_user_list = []
    for p_num_1 in range(1, npages + 1):
        data = requests.get(
            'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + code_str + '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=' + str(
                p_num_1), headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        for li_num in range(1, 11):
            str_li_num = str(li_num)
            tr_result_user = soup.select(
                'body > div > div > div.score_result > ul > li:nth-child(' + str_li_num + ') > div.score_reple > dl > dt > em:nth-child(1) > a > span')
            tr_user_point = soup.select(
                'body > div > div > div.score_result > ul > li:nth-child(' + str_li_num + ') > div.star_score > em')
            for name, rvpoint in zip(tr_result_user,tr_user_point):
                if name.text != None:
                    dic_temp = {"userId":name.text, "point":rvpoint.text}
                    docs_user_list.append(dic_temp)

    docs_movie_users = {'title': mt, 'href':movie['href'], 'user_list': docs_user_list}
    db.movie_user_list.insert_one(docs_movie_users)
    print("{} 끝!!!".format(mt))

if __name__=='__main__':
    movie_list = db.easy_movie_list.find_one({}, {'_id': False})
    pool = Pool(processes=4)
    pool.map(user_get,movie_list['list'])


