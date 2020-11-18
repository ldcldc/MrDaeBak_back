from flask import Flask, jsonify
from pakages.db_model.mysqldb_conn import conn_mysqldb
from pakages.router.test_module import test_module
from pakages.router.SignupController import signup_controller

app = Flask(__name__)
app.config["SECRET_KEY"] = "1111"
app.register_blueprint(test_module)
app.register_blueprint(signup_controller)

@app.route('/')
def index() :
    return '<h1>Mr DaeBak API Server!</h1>'


if __name__ == '__main__':
    app.run()