import cx_Oracle
import mybatis_mapper2sql
from server.mylog import MyLog

class MyDaoReply:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_comm.xml')[0]
        
    def myselect(self, bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (bbs_no,))
        list = []
        for record in rs:
            list.append({'bbs_no':record[0], 'comm_no':record[1], 'user_id':record[2], 'content':record[3], 'likes':record[4], 'dislike':record[5], 'in_date':record[6], 'in_user_id':record[7], 'up_date':record[8], 'up_user_id':record[9]})
        return list
    
    def myinsert(self, bbs_no, content, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
     
        self.cs.execute(sql, (bbs_no, user_id, content, user_id, user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def myupdate(self,user_id, pwd, user_name, mobile, email, birth, in_date, in_user_id, up_date, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (pwd, user_name, mobile, email, birth, up_user_id,user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def mydelete(self,comm_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (comm_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def likesUp(self, comm_no, user_id, like_yn):
        print("comm_no",comm_no)
        print("user_id",user_id)
        print("like_yn",like_yn)
        MyLog().getLogger().debug(comm_no)
        MyLog().getLogger().debug(user_id)
        MyLog().getLogger().debug(like_yn)
        
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, "likes_up")  
        sql = f"""merge into commlike
        using dual
            on(comm_no = {comm_no} and user_id = '{user_id}') 
        when matched then
            update set  like_yn        = '{like_yn}',
                        up_date        = to_char(sysdate, 'yyyy-mm-dd.hh24:mi:ss'),
                        up_user_id     = '{user_id}'
        when not matched then
             insert (               comm_no,
                                    user_id, 
                                    like_yn,  
                                    in_date, 
                                    in_user_id, 
                                    up_date,
                                    up_user_id) 
                        values ( {comm_no}, 
                                 '{user_id}',
                                 '{like_yn}',
                                 to_char(sysdate, 'yyyy-mm-dd.hh24:mi:ss'),
                                 '{user_id}',
                                 to_char(sysdate, 'yyyy-mm-dd.hh24:mi:ss'),
                                 '{user_id}')
                                 """
        print(sql)
        MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
     
#     def dislikeUp(self,comm_no):
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, "dislike")  
#         MyLog().getLogger().debug(sql)
#         self.cs.execute(sql, (comm_no,))
#         self.conn.commit()
#         cnt = self.cs.rowcount
#         return cnt
    
#     def mygetlike_not(self, comm_no):
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, "getlike_not")
#         MyLog().getLogger().debug(sql)
#         rs = self.cs.execute(sql, (comm_no,))
#         list = []
#         
#         for record in rs:
#             list.append({'cnt_like':record[0], 'cnt_dislike':record[1]})
#             
#         return list.cnt_like, list.cnt_dislike
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDaoReply()

    
    
    
