from ..user_management import AccountManagenent as AM
import hashlib
import bcrypt
import json
from flask import Flask, jsonify, request, Blueprint
from ..db_model.mysqldb_conn import conn_mysqldb

signup_controller = Blueprint('signup_controller', __name__)

db_conn = conn_mysqldb()
mds_db = db_conn.cursor()

# 주석 처리된건 debugging용
@signup_controller.route('/signin_db', methods=['POST'])
def signup():
    data = request.get_json()

    if request.method == 'POST':
        message, success_signup = AM.AccountManagenent.registerAccount(data, mds_db, db_conn)               
    
    return jsonify({'Success':success_signup, 'Message':message})

@signup_controller.route('/duplicate_name', methods=['POST'])
def isAvailableName():
    data = request.get_json()
    
    if request.method == 'POST':                    #AccountManagenent 호출
        message, check_dup = AM.AccountManagenent.findUserName(data['user_name'], mds_db)
    
    return jsonify({'check_name_dup':check_dup, 'Message':message})


@signup_controller.route('/duplicate_id', methods=['POST'])
def isAvailableId():
    data = request.get_json()

    if request.method == 'POST':                    #AccountManagenent 호출      
        message, check_dup = AM.AccountManagenent.findUserId(data['user_id'], mds_db)
        # print(AM.AccountManagenent.findUserId(data['user_id'], mds_db))
    
    return jsonify({'check_id_dup':check_dup, 'Message':message})
    
