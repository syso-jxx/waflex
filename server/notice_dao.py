import cx_Oracle
import mybatis_mapper2sql

class NoticeDao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_notice.xml')[0]
   
    def myselect_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        rs = self.cs.execute(sql)
        res = []
        for record in rs:
            res.append({'notice_no':record[0],'user_id':record[1],'title':record[2],
                         'content':record[3],'attach_file':record[4],'attach_path':record[5],'rdcnt':record[6],
                         'in_date':record[7],'in_user_id':record[8],'up_date':record[9],'up_user_id':record[10]})
        return res
    
    def my_search(self, title):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "search")
        
        rs = self.cs.execute(sql, (title,))
        
        res = []
        for record in rs:
            res.append({'notice_no':record[0],
                        'user_id':record[1],
                        'title':record[2],
                        'content':record[3],
                        'attach_file':record[4],
                        'attach_path':record[5],
                        'rdcnt':record[6],
                        'in_date':record[7],
                        'in_user_id':record[8],
                        'up_date':record[9],
                        'up_user_id':record[10]})
        return res
     
#      notice_no,user_id,title,content,attach_file,attach_path,rdcnt,in_date,in_user_id,up_date,up_user_id
       
    def myselect(self,notice_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        rs = self.cs.execute(sql, (notice_no,))
        obj = None
        for record in rs:
            obj = {'notice_no':record[0], 'user_id':record[1], 'title':record[2]
                        , 'content':record[3], 'attach_file':record[4], 'attach_path':record[5]
                        , 'rdcnt':record[6], 'in_date':record[7], 'in_user_id':record[8]
                        , 'up_date':record[9], 'up_user_id':record[10], 'in_user_name':record[11]}
        return obj
        
    def myinsert(self, user_id, title, content, attach_file, attach_path,  in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        self.cs.execute(sql, (user_id,title, content, attach_file, attach_path,in_user_id, up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def myupdate(self, notice_no,user_id,title,content,attach_file,attach_path,rdcnt,in_date,in_user_id,up_date,up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")
        self.cs.execute(sql, (user_id,title,content,attach_file,attach_path,up_user_id, notice_no))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def myrdcnt(self,notice_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "rdcnt")
        self.cs.execute(sql,(notice_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    

    def mydel_img(self, user_id,notice_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "mydel_img")
        self.cs.execute(sql,(user_id,notice_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

    def mydelete(self, notice_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")
        self.cs.execute(sql,(notice_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt


if __name__ == '__main__':
    dao = NoticeDao()
    list = dao.myselect('1')
    
    print(list)