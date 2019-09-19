from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import pandas as pd
from scipy import stats
import numpy as np
import json
import math
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1



for index in range(1,251):
    print(index)
    if index == 209:
        continue
    if index == 245:
        continue
    data_json = {}
    data_json['links'] = []
    data_json['nodes'] = []
    data_json['genre_data'] = []
    data_json['data'] = []

    temp_list = db.compare_movie.find({},{'_id':False})
    check = [0]*251
    movie_name = ['']*251
    array1 = []

    for x in temp_list:
        if x['movie1'] == '밴디트' or x['movie2'] == '밴디트':
            continue
        if x['movie1'] == '아메리칸 히스토리 X' or x['movie2'] == '아메리칸 히스토리 X':
            continue
        if x['movie1'] == x['movie2']:
            continue
        if x['movie1_id'] == index or x['movie2_id'] == index:
            temp_array = []
            temp_array.append(x['prob']*100)
            temp_array.append(x['movie1'])
            temp_array.append(x['movie2'])
            temp_array.append(x['total_user'])
            temp_array.append(x['same_user'])
            temp_array.append(x['movie1_id'])
            temp_array.append(x['movie2_id'])
            array1.append(temp_array)
    array1.sort(key=lambda array: array[0],reverse=True)
    print(array1)

    for i in range(0,16):
        data_json['links'].append({
            'source':array1[i][1],
            'target':array1[i][2],
            'value':array1[i][0],
            'total':array1[i][3],
            'same':array1[i][4]
        })
        check[array1[i][5]] = 1
        check[array1[i][6]] = 1
        movie_name[array1[i][5]] = array1[i][1]
        movie_name[array1[i][6]] = array1[i][2]


    genre_num = [{'title':None, 'group':0},]
    for i,name in zip(check,movie_name):
        if i == 1:
            temp_list1 = db.movie_info.find_one({'title':name},{'_id':False,'total_user':False, 'same_user':False})
            temp_list2 = db.naver_movie_list.find_one({'title':name},{'_id':False})
            num = -1
            cnt = 0
            for y in genre_num:
                cnt+=1
                if temp_list1['genre'][0] == y['title']:
                    num = y['group']
            if num == -1:
               genre_num.append({'title':temp_list1['genre'][0],'group':cnt})
               num = cnt
            data_json['nodes'].append({
                    'id': temp_list1['title'],
                    'group': num,
                    'href':temp_list2['href'],
                    'genre':temp_list1['genre'],
                    'director':temp_list1['director'],
                    'actor':temp_list1['actor']
                })
    for x in genre_num:
        if x['title'] == None:
            continue
        data_json['genre_data'].append(x)

    data_json['data'].append({'movie_n':len(movie_name),'genre_n':len(genre_num)-1})
    # json 파일 저장
    with open('./static/movie_score_'+str(index)+'.json','w',encoding='UTF-8') as outfile:
          json.dump(data_json, outfile, ensure_ascii=False, indent=4)

