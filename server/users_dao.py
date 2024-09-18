import cx_Oracle
import mybatis_mapper2sql
from server.mylog import MyLog

# user_id,user_nm,user_password,user_telno,user_email,mngr_flag,act_flag,in_date,in_user_id,up_date,up_user_id,       
class Users_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_users.xml')[0]
        
    def mydupl(self,user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_dupl")
        MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_id,))
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9],
                         'up_user_id':record[10]})
        return list
    
    def mylogin(self, user_id, user_password):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_login")
#         MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_id, user_password))
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9],
                         'up_user_id':record[10]})
            
        return list
    
    def my_kakao_login(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "kakao_login")
#         MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_id, ))
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9],
                         'up_user_id':record[10]})
            
        return list
    
    def find_id(self, user_nm, user_email):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "find_id")
#         MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_nm, user_email))
       
        id = ''
        for record in rs:
            id = record[0]
            
        return id
    
    def find_pwd(self, user_id, user_email):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "find_pwd")
#         MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_id, user_email))
       
        id = ''
        for record in rs:
            id = record[0]
            
        return id
    
    def find_pwd2(self, temp_pwd, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "find_pwd2")
#         MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (temp_pwd, user_id, user_id))
        self.conn.commit()
        
        cnt = self.cs.rowcount
        
        return cnt
    
        
    def myselect(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9],
                         'up_user_id':record[10],
                         'pay_id':record[11]})
        return list
    
    def my_search(self, user_nm):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "search")
        MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql, (user_nm,))
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9],
                         'up_user_id':record[10]})
            
        return list
    
    def my_info(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "my_info")
        MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (user_id, user_id, user_id))
        list = []
        
        for record in rs:
            list.append({'user_id':record[0],
                         'user_nm':record[1],
                         'user_password':record[2],
                         'user_telno':record[3],
                         'user_email':record[4],
                         'mngr_flag':record[5],
                         'act_flag':record[6],
                         'payday':record[7],
                         'payment_renew':record[8],
                         'in_date':record[9],
                         'in_user_id':record[10],
                         'up_date':record[11],
                         'up_user_id':record[12]})
        return list
    
    def myinsert(self, user_id,user_nm,user_password,user_telno,user_email ,mngr_flag,act_flag, in_date, in_user_id, up_date, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (user_id, user_nm, user_password, user_telno, user_email, in_user_id, up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
        
    def my_update(self, user_nm, user_password, user_telno, user_email, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (user_nm, user_password, user_telno, user_email, user_id, user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        
        return cnt
    
    def my_delete(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)

        self.cs.execute(sql, (user_id,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def mymerge_kakao(self, user_id, user_nm, user_email):
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, "merge_kakao")
        
        sql = """        
            MERGE INTO users
            using dual
            on (user_id = :1)
            when matched then
                 update set
                 user_nm = :2, 
                 user_email = :3,
                 up_date = to_char(sysdate, 'YYYY-MM-DD.HH24:MI:SS')
            when not matched then
            insert 
                (
                user_id,
                user_nm,
                user_password,
                user_telno,
                user_email,
                mngr_flag,
                act_flag,
                in_date,
                in_user_id,
                up_date,
                up_user_id
                ) 
            values 
                (
                :4, 
                :5, 
                '1111',
                '01012345678',
                :6,
                'n', 
                'y',
                to_char(sysdate, 'YYYY-MM-DD.HH24:MI:SS'),  
                :7,
                to_char(sysdate, 'YYYY-MM-DD.HH24:MI:SS'),  
                :8
                )
            """
        
        self.cs.execute(sql, (user_id,user_nm,user_email,user_id,user_nm,user_email,user_id,user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        

if __name__ == "__main__":
    dao = Users_dao()   
    
    