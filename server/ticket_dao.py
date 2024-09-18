import cx_Oracle
import mybatis_mapper2sql
from server.mylog import MyLog

class Ticket_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_ticket.xml')[0]
        
# ticket_no,name,price,in_date,in_user_id,up_date,up_user_id        
        
    def myselect_all(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_all")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'ticket_no':record[0],
                         'name':record[1],
                         'price':record[2], 
                         'in_date':record[3],
                         'in_user_id':record[4],
                         'up_date':record[5],
                         'up_user_id':record[6]})
        return list
    
    def myselect(self, ticket_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(ticket_no,))
        
        obj = None
        for record in rs:
            obj = {'ticket_no':record[0],
                   'name':record[1],
                   'price':record[2], 
                   'in_date':record[3],
                   'in_user_id':record[4],
                   'up_date':record[5],
                   'up_user_id':record[6]}
        return obj
    
    def myinsert(self, name, price,in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (name, price, in_user_id, up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def myupdate(self, ticket_no, name, price, in_date, in_user_id, up_date, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (name, price, in_user_id, ticket_no))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def mydelete(self,ticket_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete") 
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (ticket_no,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = Ticket_dao()

    