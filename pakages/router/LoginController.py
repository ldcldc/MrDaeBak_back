from ..db_model.mysqldb_conn import conn_mysqldb
from ..user_management import UserConstructor as UC

from flask import Flask, flash, jsonify, request, render_template, session, Blueprint
import bcrypt
import jwt
import pymysql

signup_controller = Blueprint('login_controller', __name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"

def isValidAccount(login_info):                                 #로그인 정보 확인 함수
    #print('in isValidAccount()')
    user_id = login_info['user_id']                             #입력된 정보 분류 
    password = login_info['user_password']
    #print(user_id, password)

    db_conn = conn_mysqldb()                                    #db 연결
    cursor = db_conn.cursor()
    
    sql = "SELECT * FROM user_info WHERE user_id=%s"            #입력된 id와 맞는 유저 검색
    rows_count = cursor.execute(sql,user_id)
    db_conn.close()                                             #db연결 해제
    #print(rows_count)
    if rows_count > 0:                                          #입력된 id가 db에 있을때
        user_info = cursor.fetchone()
        #print(user_info)

        is_pw_correct = bcrypt.checkpw(password.encode('UTF-8'), user_info[2].encode('UTF-8'))     #비밀번호 비교 
        #print(is_pw_correct)
        if is_pw_correct:                                       #비밀번호 같으면 user_info return
            return user_info
    return None

    



@login_controller.route('/login', methods=['POST'])
def login():
    #print('in login()')
    if request.method == 'POST':
        #print(request.form)                         
        user_info = isValidAccount(request.form)    #user_info 받아옴  user_info[0] = id, [1] = name, [2] = pw
        #print('in login()')                         # [3] = address, [4] = ordered_num, [5] = class
        if not user_info == None:
            if user_info[5] == 'member':            #class = member
                message, success_login, access_token = UC.UserConstructor.loginAsMember(user_info)
                #print('in login()')
            elif user_info[5] == 'manager':         #class = manager
                message, success_login, access_token = UC.UserConstructor.loginAsManager(user_info)
                #print('in login()')
        else:                                       #login 실패시
            message = 'Invalid Params' 
            success_login = 'false'
            access_token = ''
            user = ''

        #print(message, success_login, access_token)
    return jsonify({'Message':message, 'Success':success_login, 'User_id':user_info[0], 'User_name':user_info[1],\
                    'Class':user_info[5], 'access_token':access_token})

@login_controller.route('/logout')
def logout():
    #아직 안됨
    return jsonify({'Success':'true'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
