import numpy as np 
import pandas as pd
import cx_Oracle

class reco_algo:
    def __init__(self):
        # 모든 영화 (movie table)
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.meta = pd.read_sql('select * from movie', self.conn)
        self.meta = self.meta[['MOVIE_NO', 'TITLE', 'GENRE_CODE']]
        self.meta = self.meta.rename(columns={'MOVIE_NO':'movie_id'})
        self.meta = self.meta.rename(columns={'TITLE':'movie_name'})
        self.meta = self.meta.rename(columns={'GENRE_CODE':'genres'})
        
        # 유저별 평가 테이블(evl table)
        self.ratings = pd.read_sql('select * from evl', self.conn)
        self.ratings = self.ratings[['USER_ID', 'MOVIE_NO', 'RATE']]
        self.ratings = self.ratings.rename(columns={'USER_ID':'user_id'})
        self.ratings = self.ratings.rename(columns={'MOVIE_NO':'movie_id'})
        self.ratings = self.ratings.rename(columns={'RATE':'rating'})
        
        # 값 숫자로 변환
        self.meta.movie_id = pd.to_numeric(self.meta.movie_id, errors='coerce')
        self.ratings.movie_id = pd.to_numeric(self.ratings.movie_id, errors='coerce')
         
        # 영화 테이블, 평점 테이블 inner조인
        self.data = pd.merge(self.ratings, self.meta, on='movie_id', how='inner')
        self.matrix = self.data.pivot_table(index='user_id', columns='movie_name', values='rating')
        
        # 장르 가중치
        self.GENRE_WEIGHT = 0.3
        
    # 피어슨 상관관계 함수 
    def pearsonR(self, s1, s2):
        s1_c = s1 - s1.mean()
        s2_c = s2 - s2.mean()
        return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
 
    # 영화 추천 함수 (input : 영화 제목, 기준 테이블, 몇개 영화 추천 받을 것인지, 비슷한 장르에 가중치 받을 것인지)
    def recommend(self, input_movie, matrix, n, similar_genre = True):
        input_genres = self.meta[self.meta['movie_name'] == input_movie]['genres'].iloc(0)[0]
        
        result = []  
        # 같은 이름의 영화 건너뛰기
        for title in matrix.columns:
            if title == input_movie:
                continue
     
            # 피어슨 상관관계 함수를 이용해 기준 테이블과 비교
            cor = self.pearsonR(matrix[input_movie], matrix[title])
            print(cor)
             
            # input으로 넣은 영화의 장르와 비교할 대상의 장르가 같으면 가중치를 줌
            if similar_genre and len(input_genres) > 0:
                temp_genres = self.meta[self.meta['movie_name'] == title]['genres'].iloc(0)[0]
      
                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (self.GENRE_WEIGHT * same_count)
             
            if np.isnan(cor):
                continue
            else:
                result.append((title, '{:.2f}'.format(cor), temp_genres))
                 
        result.sort(key=lambda r: r[1], reverse=True)
     
        return result[:n]
 
# # 결과
# if __name__ == '__main__':
#     rc = reco_algo()
#     result = rc.recommend('미션 파서블 (MISSION: POSSIBLE)', rc.matrix, 10, similar_genre = True)
#     for re in result:
#         print(re[0])
#     


