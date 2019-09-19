from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbProject1

movie_list = db.easy_movie_list.find_one({}, {'_id': False})

movies = []
cnt = 0
for mt in movie_list['list']:

    cnt += 1
    user_list = db.movie_user_list.find_one({'title': mt['title'], 'href': mt['href']}, {'_id': False})
    user_over_4 = []
    for user in user_list['user_list']:
        ok = True
        for i in user_over_4:
         if i == user['userId']:
             ok = False
             break
        if ok == True:
            user_over_4.append(user['userId'])
    movie = {'title': mt['title'], 'href': mt['href'], 'movie_id': cnt, 'user_list': user_over_4}
    print(movie)
    movies.append(movie)

db.refine_user_list.insert_many(movies)