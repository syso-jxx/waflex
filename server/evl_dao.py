import cx_Oracle
import mybatis_mapper2sql
# from server.mylog import MyLog

class Evl_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_evl.xml')[0]
        
    def select_evl(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_evl')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (user_id, ))
             
        list = []
        
        for record in rs:
            list.append({'movie_no':record[0],
                         'title':record[1],
                         'release_date':record[2],
                         'nation_name':record[3],
                         'genre_name':record[4],
                         'director':record[5],
                         'rate':record[6]})
        return list
    
    def check_vali(self, user_id, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'check_vali')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (user_id, movie_no))
             
        list = []
        
        for record in rs:
            list.append(record[0])
            
        return list
    
    def select_all(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_all')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'movie_no':record[1],
                         'rate':record[2],
                         'in_date':record[3],
                         'in_user_id':record[4],
                         'up_date':record[5], 
                         'up_user_id':record[6]})
        return list
  
    def insert(self, user_id, movie_no, in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, movie_no, in_user_id, up_user_id))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def update(self, rate, user_id, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (rate, user_id, user_id, movie_no))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def delete(self, user_id, movie_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, movie_no ))
         
        cnt = self.cs.rowcount   
        
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.commit()
        self.conn.close()

