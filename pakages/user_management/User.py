from abc import *
from random import randint
from ..db_model.mysqldb_conn import conn_mysqldb

class User(metaclass=ABCMeta):
    id = ''
    name = ''
    classification = ''
    address = ''

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getClass(self):
        return self.classification

    def getAddress(self):
        return self.address
    
    def setAddress(self, new_address):
        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        sql = """
                UPDATE user_info 
                SET address=%s 
                WHERE user_id=%s
                """

        db_cursor.execute(sql, (new_address, self.id))
        db_conn.commit()
        db_conn.close()


class Member(User):
    def __init__(self, user_info):
        self.id = user_info['user_id']
        self.name = user_info['user_name']
        self.classification = user_info['class']
        self.address = user_info['address']
        self.ordered_num = user_info['ordered_num']
        self.ordered_num_added = False
    
    def getOrderNum(self):
        return self.ordered_num

    def addOrderNum(self):
        self.ordered_num += 1
        self.ordered_num_added = True

        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        sql = """
                UPDATE user_info 
                SET ordered_num=%s
                WHERE user_id=%s
                """

        db_cursor.execute(sql, (self.ordered_num, self.id))
        db_conn.commit()
        db_conn.close()
    
    def setClass(self):
        '''
        디너 주문 완료시 호출하며 ordered_num이 15회가 되는 순간 classification이 vip로 바뀌도록 한다.
        반드시 addOrderNum 메서드가 먼저 호출 되어야 한다.
        '''

        if not self.ordered_num_added:
            raise Exception('ooder_num has not been added.')

        if self.classification == 'member' and self.ordered_num >= 15:
            self.classification = 'vip'

            db_conn = conn_mysqldb()
            db_cursor = db_conn.cursor()

            sql = """
                    UPDATE user_info 
                    SET class=%s
                    WHERE user_id=%s
                    """

            db_cursor.execute(sql, ('vip', self.id))
            db_conn.commit()
            db_conn.close()

class Guest(User):
    def __init__(self):
        self.classification = 'guest'
        self.constructTmpId()

    def constructTmpId(self):
        uniq = False
        tmp_id = 0

        db_conn = conn_mysqldb()
        db_cursor = db_conn.cursor()

        while not uniq:
            tmp_id = randint(0000000, 9999999)

            sql = """
                    SELECT *
                    FROM user_info
                    WHERE user_id=%s
                    """
            cnt = db_cursor.execute(sql, str(tmp_id))

            if not cnt:
                uniq = True

        self.id = str(tmp_id)
        self.name = 'guest' + self.id

        sql = """
                INSERT INTO user_info 
                (user_name, user_id, class) 
                VALUES (%s, %s, 'guest')
                """
        
        db_cursor.execute(sql, (self.name, self.id))
        db_conn.commit()
        db_conn.close()

class Manager(User):
    def __init__(self, user_info):
        self.id = user_info['user_id']
        self.name = user_info['user_name']
        self.classification = 'manager'