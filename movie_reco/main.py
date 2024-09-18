import numpy as np 
import pandas as pd
import cx_Oracle

# 모든 영화 (movie table)
conn = cx_Oracle.connect("username", "password", "dsn")
cs = conn.cursor()
sql = 'select * from movie'
 
meta = pd.read_sql(sql, conn)

meta = meta[['MOVIE_NO', 'TITLE', 'GENRE_CODE']]

meta = meta.rename(columns={'MOVIE_NO':'movie_id'})
meta = meta.rename(columns={'TITLE':'movie_name'})
meta = meta.rename(columns={'GENRE_CODE':'genres'})


# 유저별 평가 테이블(evl table)
sql = 'select * from evl'
ratings = pd.read_sql(sql, conn)

ratings = ratings[['USER_ID', 'MOVIE_NO', 'RATE']]
ratings = ratings.rename(columns={'USER_ID':'user_id'})
ratings = ratings.rename(columns={'MOVIE_NO':'movie_id'})
ratings = ratings.rename(columns={'RATE':'rating'})

# 값 숫자로 변환
meta.movie_id = pd.to_numeric(meta.movie_id, errors='coerce')
ratings.movie_id = pd.to_numeric(ratings.movie_id, errors='coerce')
 
# 영화 테이블, 평점 테이블 inner조인
data = pd.merge(ratings, meta, on='movie_id', how='inner')
matrix = data.pivot_table(index='user_id', columns='movie_name', values='rating')
 
# 피어슨 상관관계 함수 
def pearsonR(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
 
GENRE_WEIGHT = 0.1
# 영화 추천 함수 (input : 영화 제목, 기준 테이블, 몇개 영화 추천 받을 것인지, 비슷한 장르에 가중치 받을 것인지)
def recommend(input_movie, matrix, n, similar_genre = True):
    input_genres = meta[meta['movie_name'] == input_movie]['genres'].iloc(0)[0]
 
    result = []  
    # 같은 이름의 영화 건너뛰기
    for title in matrix.columns:
        if title == input_movie:
            continue
 
        # 피어슨 상관관계 함수를 이용해 기준 테이블과 비교
        cor = pearsonR(matrix[input_movie], matrix[title])
         
        # input으로 넣은 영화의 장르와 비교할 대상의 장르가 같으면 가중치를 줌
        if similar_genre and len(input_genres) > 0:
            temp_genres = meta[meta['movie_name'] == title]['genres'].iloc(0)[0]
  
            same_count = np.sum(np.isin(input_genres, temp_genres))
            cor += (GENRE_WEIGHT * same_count)
         
        if np.isnan(cor):
            continue
        else:
            result.append((title, '{:.2f}'.format(cor), temp_genres))
             
    result.sort(key=lambda r: r[1], reverse=True)
 
    return result[:n]
 
# 결과
result = recommend('기생충 (PARASITE)', matrix, 10, similar_genre = True)
for re in result:
    print(re[0])
    
# print(pd.DataFrame(recommend_result, columns = ['Title', 'Correlation', 'Genre']))


