import hashlib
import bcrypt
from flask import Flask, jsonify, request

class AccountManagenent:
    @staticmethod
    def findUserName(username, mds_db):
        #print('in findUserName()')
        message = ''                                #상황에 따른 메시지
        check_dup = 'true'                          #중복확인 성공 여부

        username = username.strip()                 #좌우 공백 제거
        if not username:                                            #name 썼는지 확인
            check_dup = 'false'
            message = 'Need Name'

        else :
            sql = 'SELECT * from user_info where user_name=%s'      #닉네임 중복 확인
            cnt = mds_db.execute(sql, username)

            if cnt:                                                 #중복
                check_dup = 'false'
                message = 'Unavailable Name'

            else:                                                   #안중복
                message = 'available Name'

        return [message] + [check_dup]                              #json으로 보낼 데이터 return


    @staticmethod
    def findUserId(userid, mds_db):
        #print('in findUserId()')
        message = ''                                #상황에 따른 메시지
        check_dup = 'true'                          #중복확인 성공 여부

        id = userid.strip()                         #좌우 공백 제거          
        if not id:                                                  #id 썼는지 확인
            check_dup = 'false'
            message = 'Need Id'
        else:
            sql = 'SELECT * from user_info where user_id=%s'        #id 중복 확인
            cnt = mds_db.execute(sql, id)

            if cnt:                                                 #중복
                check_dup = 'false'
                message = 'Unavailable Id'

            else:                                                   #안중복
                message = 'available Id'

        return [message] + [check_dup]                              #json으로 보낼 데이터 return


    @staticmethod
    def registerAccount(user_info, mds_db, db_conn):
        #print('in registerAccount()')
        message = ''                                #상황에 따른 메시지
        success_signup = 'true'                     #회원가입 성공 여부
        
        username = user_info['user_name'].strip()       #좌우 공백 제거
        id = user_info['user_id'].strip()
        password = user_info['user_password'].strip()
                                                    
        if not username or not id or not password:      #안쓴거 있나 확인
            success_signup = 'false'
            message = 'Insert Error'

        if user_info['check_name_dup'] == 'false':      #닉네임 중복확인 여부
            success_signup = 'false'
            message = 'Check Name Duplicate'

        if user_info['check_id_dup'] == 'false':        #id 중복확인 여부
            success_signup = 'false'
            message = 'Check Id Duplicate'

        if success_signup == 'true':                    #데이터 문제 없음
            password = bcrypt.hashpw(user_info['user_password'].encode('utf-8'),bcrypt.gensalt())   #비밀번호 hash
            #print(password)
            sql = """INSERT INTO user_info (user_name, user_id, password) VALUES (%s, %s, %s);"""   #db에 저장
            mds_db.execute(sql, (username, id, password))
            db_conn.commit() 

            message = 'Success signup'                  #회원가입 성공
        
        return [message] + [success_signup]
