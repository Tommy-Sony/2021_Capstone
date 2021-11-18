import os
from database import db
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def basic():
    return render_template("main.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/search_result')
def search_result():
    return render_template("search_result.html")

@app.route('/config')
def config():
    return render_template("configuration.html")

###############################################
# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()
###############################################

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # debug = True -> 코드 수정할 때마다 Flask가 인식해서 다시 시작


