from flask import Flask, jsonify
from db_model.mysqldb_conn import conn_mysqldb

app = Flask(__name__)

@app.route('/')
def index() :
    return '<h1>Hello!!</h1>'


# @app.route('/db_test', methods=['get']) 
# def db_test():
#     db = conn_mysqldb()
#     db_cursor = db.cursor()
#     sql = "select * from user_info"
#     db_cursor.execute(sql)
#     user_row = db_cursor.fetchone()

#     user = {
#         'user_id' : user_row[0],
#         'user_name' : user_row[1],
#         'user_pw' : user_row[2],
#         'address' : user_row[3],
#         'ordered' : user_row[4],
#         'class' : user_row[5]
#     }

#     return jsonify(user)



app.run()