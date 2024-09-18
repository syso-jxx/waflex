import cx_Oracle
import mybatis_mapper2sql
# from server.mylog import MyLog

class Reco_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_reco.xml')[0]
        
    def select_reco(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_reco')
#         MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (user_id, ))
        
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
  
    def insert(self, user_id, title, in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, title, in_user_id, up_user_id))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def delete(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id,))
         
        cnt = self.cs.rowcount   
        
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.commit()
        self.conn.close()
        
