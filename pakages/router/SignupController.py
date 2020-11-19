from ..user_management import AccountManagenent as AM
import hashlib
import bcrypt
from flask import Flask, jsonify, request, Blueprint
from ..db_model.mysqldb_conn import conn_mysqldb

signup_controller = Blueprint('signup_controller', __name__)

db_conn = conn_mysqldb()
mds_db = db_conn.cursor()

# 주석 처리된건 debugging용
@signup_controller.route('/signin_db', methods=['POST'])
def signup():
    #print('in signup()')
    if request.method == 'POST':
    #    print(request.form)
        message, success_signup = AM.AccountManagenent.registerAccount(request.form, mds_db, db_conn)               
    #print(message)
    #print(success_signup)
    #return render_template('signin_test.html', user_name = request.form['user_name'], \
    #    user_id = request.form['user_id'], user_password = request.form['user_password'])
    return jsonify({'Success':success_signup, 'Message':message})

@signup_controller.route('/duplicate_name', methods=['POST'])
def isAvailableName():
    #print('in isAvailableName()')
    if request.method == 'POST':                    #AccountManagenent 호출
        message, check_dup = AM.AccountManagenent.findUserName(request.form['user_name'], mds_db)
    #print(message)
    #print(check_dup)
    #return render_template('signin_test.html', user_name = request.form['user_name'], \
    #    user_id = request.form['user_id'], user_password = request.form['user_password'], check_name_dup = check_dup)
    return jsonify({'check_name_dup':check_dup, 'Message':message})


@signup_controller.route('/duplicate_id', methods=['POST'])
def isAvailableId():
    #print('in isAvailableId()')
    if request.method == 'POST':                    #AccountManagenent 호출      
        message, check_dup = AM.AccountManagenent.findUserId(request.form['user_id'], mds_db)
    #print(message)
    #print(check_dup)
    #return render_template('signin_test.html', user_name = request.form['user_name'], \
    #    user_id = request.form['user_id'], user_password = request.form['user_password'], check_id_dup = check_dup)
    return jsonify({'check_id_dup':check_dup, 'Message':message})
