import cx_Oracle
import mybatis_mapper2sql
# from server.mylog import MyLog

class Payment_dao:
    def __init__(self):
        conn = cx_Oracle.connect("username", "password", "dsn")
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_payment.xml')[0]
        
    def check(self, user_id, ticket_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'check')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql, (user_id, ticket_no))
             
        list = []
        
        for record in rs:
            list.append({'payday':record[0],
                         'payment_flag':record[1],
                         'payment_renew':record[2],
                         'in_date':record[3],
                         'in_user_id':record[4],
                         'up_date':record[5], 
                         'up_user_id':record[6]})
            
        return list
    
    def select_all(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select_all')
#         MyLog().getLogger().debug(sql)
        
        rs = self.cs.execute(sql)
        
        list = []
        for record in rs:
            list.append({'user_id':record[0],
                         'ticket_no':record[1],
                         'name':record[2],
                         'price':record[3],
                         'payday':record[4],
                         'payment_flag':record[5],
                         'payment_renew':record[6],
                         'in_date':record[7],
                         'in_user_id':record[8],
                         'up_date':record[9], 
                         'up_user_id':record[10]})
        return list
  
    def insert(self, user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, user_id, user_id))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def update(self, user_id, ticket_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, user_id, ticket_no))
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def merge_payment(self, user_id, ticket_no):
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'merge_payment')
#         MyLog().getLogger().debug(sql)

        sql = f'''MERGE INTO payment
            using dual
            on (user_id = '{user_id}' and ticket_no = {ticket_no})
            when matched then
                 update set
                    payday  = to_char(sysdate,'DD'),
                    payment_flag      = 'y',
                    payment_renew     = to_char(sysdate + 30,'YYYY-MM-DD'),
                    up_date         = to_char(sysdate,'YYYY-MM-DD.HH24:MI:SS'),
                    up_date_id      = '{user_id}'
            when not matched then
                insert(
                    user_id,
                    ticket_no,
                    payday,
                    payment_flag,
                    payment_renew,
                    in_date,
                    in_user_id,
                    up_date,
                    up_date_id
                ) values(
                    '{user_id}',
                    {ticket_no},
                    to_char(sysdate,'DD'),
                    'y',
                    to_char(sysdate + 30,'YYYY-MM-DD'),                 
                    to_char(sysdate,'YYYY-MM-DD.HH24:MI:SS'),
                    '{user_id}',
                    to_char(sysdate,'YYYY-MM-DD.HH24:MI:SS'),
                    '{user_id}'
                )
                '''
        
        self.cs.execute(sql)
         
        cnt = self.cs.rowcount
        
        return cnt
    
    def delete(self, user_id, ticket_no):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
#         MyLog().getLogger().debug(sql)
        
        self.cs.execute(sql, (user_id, ticket_no))
         
        cnt = self.cs.rowcount   
        
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.commit()
        self.conn.close()

