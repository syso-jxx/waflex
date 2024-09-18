import cx_Oracle
import mybatis_mapper2sql
from server.mylog import MyLog

class MyDaoCommunity:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bbs.xml')[0]
        
    def myselect_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'bbs_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],'writer':record[7],'in_date':record[8],'in_user_id':record[9],'up_date':record[10],'up_user_id':record[11]})
        return list
    
    def myselect(self, bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (bbs_no,))
        print(rs)
        obj = None
        for record in rs:
            obj = {'bbs_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],'writer':record[7],'in_date':record[8],'in_user_id':record[9],'up_date':record[10],'up_user_id':record[11]}
        return obj
    
    def my_search(self, title):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "search")
        
#         MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (title,))

        list = []
        for record in rs:
            list.append({'bbs_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],'writer':record[7],'in_date':record[8],'in_user_id':record[9],'up_date':record[10],'up_user_id':record[11]})
            
        return list
    
    
    def myinsert(self, user_id, title, content, attach_file, attach_path, writer):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
    
        self.cs.execute(sql, (user_id, title, content, attach_file, attach_path, writer, user_id, user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        
        return cnt

    def comm_ins(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_ins")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (user_id,))
        print(rs)
        obj = None
        for record in rs:
            obj = {'bbs_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],'writer':record[7],'in_date':record[8],'in_user_id':record[9],'up_date':record[10],'up_user_id':record[11]}
        return obj
        
    def myupdate(self, bbs_no, user_id, title, content, attach_file, attach_path):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (user_id, title, content, attach_file, attach_path, bbs_no))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def rdcntUp(self, bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "rdcntup")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bbs_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def showlist(self, bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (bbs_no,))
        print(rs)
        list = []
        for record in rs:
            list.append({'bbs_no':record[0],'user_id':record[1],'title':record[2],'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],'writer':record[7],'in_date':record[8],'in_user_id':record[9],'up_date':record[10],'up_user_id':record[11]})
        return list
    
    def mydelete_bbsReply(self,bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete_reply")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bbs_no, ))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def mydelete(self,bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bbs_no, ))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def mydel_img(self, user_id,bbs_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "mydel_img")
        self.cs.execute(sql,(user_id,bbs_no))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDaoCommunity()

    
    
    