from flask import Flask, jsonify
from db_model.mysqldb_conn import conn_mysqldb
from router.test_module import test_module

app = Flask(__name__)
app.register_blueprint(test_module)

@app.route('/')
def index() :
    return '<h1>Mr DaeBak API Server!</h1>'


if __name__ == '__main__':
    app.run()