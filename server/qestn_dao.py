import cx_Oracle
import mybatis_mapper2sql
from server.mylog import MyLog

# user_id,user_nm,user_password,user_telno,user_email,mngr_flag,act_flag,in_date,in_user_id,up_date,up_user_id,       
class Qestn_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_qestn.xml')[0]
        
    def myselect_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
#         MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'qestn_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'writer':record[4],'answer':record[5],'answrr':record[6],'in_date':record[7],'id_user_id':record[8],'up_date':record[9],'up_user_id':record[10]})
        return list
    
    def myselect_qnalist(self,user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_qnalist")
#         MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (user_id,))
        list = []
        for record in rs:
            list.append({'qestn_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'writer':record[4],'answer':record[5],'answrr':record[6],'in_date':record[7],'id_user_id':record[8],'up_date':record[9],'up_user_id':record[10],'in_user_name':record[11]})
        return list
    
    def myselect(self, qestn_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
#         MyLog().getLogger().debug(sql)

        rs = self.cs.execute(sql,(qestn_no,))
        obj = None
        for record in rs:
            obj = {'qestn_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'writer':record[4],'answer':record[5],'answrr':record[6],'in_date':record[7],'id_user_id':record[8],'up_date':record[9],'up_user_id':record[10],'in_user_name':record[11]}
        return obj
    
    def myinsert(self,qestn_no, user_id, title, content, writer, answer):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (user_id, title, content,))
        cnt = self.cs.rowcount
        return cnt
    
    def myupdate_answer(self, qestn_no, user_id, answer, up_date, writer):
        sql  = mybatis_mapper2sql.get_child_statement(self.mapper, "update_answer")
#         self.mylog.logger.debug(sql)
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(answer, writer, qestn_no,))
        cnt = self.cs.rowcount
        return cnt
    
    def mydel_answer(self, qestn_no):
        sql  = mybatis_mapper2sql.get_child_statement(self.mapper, "del_answer")
#         self.mylog.logger.debug(sql)
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(qestn_no,))
        cnt = self.cs.rowcount
        return cnt
    
    
    def mydelete(self, qestn_no):
        sql  = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")
#         self.mylog.logger.debug(sql)
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(qestn_no,))
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self):
#         print("파괴자")
        self.conn.commit() 
        self.cs.close()
        self.conn.close()