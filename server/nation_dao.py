import cx_Oracle
import mybatis_mapper2sql
# from server.mylog import MyLog

class Nation_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_nation.xml')[0]
        
    def select_all(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_all')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)

        list = []
        for record in rs:
            list.append({'nation_code':record[0],
                         'name':record[1],
                         'in_date':record[2],
                         'in_user_id':record[3],
                         'up_date':record[4],
                         'up_user_id':record[5]})
        
        return list
    
    def select_one(self, nation_code):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_one')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (nation_code, ))
        
        list = []
        for record in rs:
            list.append({'nation_code':record[0],
                         'name':record[1],
                         'in_date':record[2],
                         'in_user_id':record[3],
                         'up_date':record[4],
                         'up_user_id':record[5]})
        
        return list
  
    def update(self, nation_code, name, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
#         MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (nation_code, name, up_user_id, nation_code))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def insert(self, nation_code, name, in_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (nation_code, name, in_user_id, in_user_id))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def delete(self, nation_code):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (nation_code, ))
         
        cnt = self.cs.rowcount   
        
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.commit()
        self.conn.close()

