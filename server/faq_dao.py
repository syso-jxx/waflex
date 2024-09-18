import cx_Oracle
import mybatis_mapper2sql
# faq_no,user_id,title,content,writer,in_date,in_user_id,up_date,up_user_id

class faqDAO:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_faq.xml')[0]
   
    def myselect_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        rs = self.cs.execute(sql)
        res = []
        for record in rs:
            res.append({'faq_no':record[0],'user_id':record[1],'title':record[2],
                         'content':record[3],'writer':record[4],
                         'in_date':record[5],'in_user_id':record[6],'up_date':record[7],'up_user_id':record[8]})
        return res
     
       
    def myselect(self,faq_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        rs = self.cs.execute(sql, (faq_no,))
        obj = None
        for record in rs:
            obj = {'faq_no':record[0],'user_id':record[1],'title':record[2],
                         'content':record[3],'writer':record[4],
                         'in_date':record[5],'in_user_id':record[6],
                         'up_date':record[7],'up_user_id':record[8], 'in_user_name':record[9]}
        return obj
        
    def myinsert(self, user_id,title,content,writer,in_user_id,up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        self.cs.execute(sql, (user_id,title,content,writer,in_user_id,up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def myupdate(self, faq_no,user_id,title,content,writer,in_date,in_user_id,up_date,up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")
        self.cs.execute(sql, (user_id,title,content,writer,up_user_id,faq_no))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
 

    def mydel_img(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "mydel_img")
        self.cs.execute(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

    def mydelete(self, faq_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")
        self.cs.execute(sql,(faq_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt


if __name__ == '__main__':
    dao = faqDAO()
    cnt = dao.mydelete('1')    
    print(cnt)