import os
from database import db
import pymysql
from flask import Flask, render_template , request

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

@app.route('/search_result',methods=['POST'])
def search_store():
    #result => 가게명(keyword) 이용해 DB 검색한 결과
    result= request.form['keyword']
    connect_db = pymysql.connect(host='localhost', user='root', db='capstone', password='0000', charset='utf8')
    curs = connect_db.cursor()
    sql = "SELECT store_name, pos_rate, pos_keyword FROM kakao_review where store_name LIKE %s"
    curs.execute(sql,("%" + result + "%"))
    sql_result = curs.fetchall()
    posts = []
    hashtag = []

    if not sql_result:
        print()
        #검색결과 없음 페이지
    else:
        originalList = ("".join(sql_result[0][2])).split(', ')
        hashtagList = ["#"+x for x in originalList]

        sql_result_dict = {}
        sql_result_dict['author'] = {
                'storename': sql_result[0][0]
        }
        sql_result_dict['rank'] = str(int(sql_result[0][1]*100)) + "%"
        sql_result_dict['review'] = ' '.join(hashtagList)
        posts.append(sql_result_dict)

    return render_template("search_result.html", posts=posts)
    #return render_template("search_result.html",result=result)

###############################################
# 현재있는 파일의 디렉토리 절대경로


###############################################

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    #127.0.0.1
    # debug = True -> 코드 수정할 때마다 Flask가 인식해서 다시 시작
