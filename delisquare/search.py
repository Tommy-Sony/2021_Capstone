from flask import Flask,render_template
from flask import request
from app import app


@app.route('/search_result',methods=['POST'])
def search_store():
    result= request.form
    return render_template("search_result.html")
    #value= request.form['input']
    #msg = "%s 검색결과입니다" %value
    #return msg
