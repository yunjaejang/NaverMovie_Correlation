import requests
from bs4 import BeautifulSoup
import asyncio
from multiprocessing import Pool
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1



Check = [[0]*311 for i in range(311)]


def comp_user(movie1):
    movies = db.refine_user_list.find({},{'_id':False},no_cursor_timeout = True)
    # docs = []
    print('{} 시작!!'.format(movie1['title']))
    for movie2 in movies:
        if movie1 == movie2:
            continue
        movie1_id = movie1['movie_id']
        movie2_id = movie2['movie_id']
        if (db.compare_movie.find_one({'movie1_id':movie1_id,'movie2_id':movie2_id}) != None) or (db.compare_movie.find_one({'movie1_id':movie2_id,'movie2_id':movie1_id})!=None):
            continue

        same_user = 0
        index1 = 0
        check1 = [0]*(len(movie1['user_list'])+2)
        check2 = [0]*(len(movie2['user_list'])+2)
        for user_name1 in movie1['user_list']:
            index2 = 0
            for user_name2 in movie2['user_list']:
                if user_name1 == user_name2 and check1[index1] == 0 and check2[index2] == 0:
                    check1[index1] = check2[index2] = 1
                    same_user+=1
                    break
                index2+=1
            index1 += 1
        total_user = len(movie1['user_list'])+len(movie2['user_list'])-same_user
        doc = {'movie1':movie1['title'],'movie2':movie2['title'],'movie1_id':movie1_id,'movie2_id':movie2_id,'movie1_href':movie1['href'],'movie2_href':movie2['href'],'total_user':total_user,'same_user':same_user,'prob':float(same_user/total_user)}
        print(doc)
        db.compare_movie.insert_one(doc)
    print('{} 끝!!!'.format(movie1['title']))



if __name__ == '__main__':
    movies = db.refine_user_list.find({},{'_id':False},no_cursor_timeout = True)
    pool = Pool(processes=4)
    pool.map(comp_user, movies)




