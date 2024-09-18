import cx_Oracle
import mybatis_mapper2sql
# from server.mylog import MyLog

class Movie_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_movie.xml')[0]
        
    def select_search(self, title):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_search')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (title,))
        
        list = []
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_name':record[1],
                         'nation_name':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
    
    def select_all(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_all')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_name':record[1],
                         'nation_name':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
    
    def select_all_admin(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_all_admin')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_name':record[1],
                         'nation_name':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
    
    def select_list(self, sel_genre, sel_nation, sel_reco):
        sql = f"""SELECT 
                    movie_no,
                    (select name
                       from genre
                      where movie.genre_code = genre.genre_code) genre_name,
                    (select name
                       from nation
                      where nation.nation_code = movie.nation_code) nation_name,
                    title,
                    director,
                    actor,
                    runtime,
                    release_date,
                    poster,
                    url,
                    stream_cnt,
                    in_date,
                    in_user_id,
                    up_date,
                    up_user_id
                from 
                    movie
                where
                    genre_code like '{sel_genre}%'
                  and
                      nation_code like '{sel_nation}%'
                order by {sel_reco}
                """

#        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_list')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_name':record[1],
                         'nation_name':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
    
    def select_one(self, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_one')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (movie_no,))
        
        list = []
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_code':record[1],
                         'nation_code':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
    
    def select_ten(self):
        sql = f"""SELECT 
                    movie_no,
                    (select name
                       from genre
                      where movie.genre_code = genre.genre_code) genre_name,
                    (select name
                       from nation
                      where nation.nation_code = movie.nation_code) nation_name,
                    title,
                    director,
                    actor,
                    runtime,
                    release_date,
                    poster,
                    url,
                    stream_cnt,
                    in_date,
                    in_user_id,
                    up_date,
                    up_user_id
                from 
                    movie
                where
                    rownum <= 10
                order by stream_cnt desc
                """
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        for record in rs:
            list.append({'movie_no':record[0],
                         'genre_name':record[1],
                         'nation_name':record[2],
                         'title':record[3],
                         'director':record[4],
                         'actor':record[5],
                         'runtime':record[6],
                         'release_date':record[7],
                         'poster':record[8],
                         'url':record[9],
                         'stream_cnt':record[10],
                         'in_date':record[11],
                         'in_user_id':record[12],
                         'up_date':record[13],
                         'up_user_id':record[14]})
        
        return list
        
    def insert(self, genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
#         MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, in_user_id, up_user_id))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def update_all(self, genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, up_user_id, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update_all')
#         MyLog().getLogger().debug(sql)
          
        self.cs.execute(sql, (genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, up_user_id, movie_no))
          
        cnt = self.cs.rowcount     
         
        return cnt    
    
    def update_stream_cnt(self, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update_stream_cnt')
#         MyLog().getLogger().debug(sql)
          
        self.cs.execute(sql, (movie_no, ))
          
        cnt = self.cs.rowcount     
         
        return cnt    
    
    def delete(self, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (movie_no, ))
         
        cnt = self.cs.rowcount   
        
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.commit()
        self.conn.close()

