import json
import pymysql
import pandas as pd

##### db 연결 #####
connect_db = pymysql.connect(
    user='root',
    passwd='0000', #비밀번호
    host='127.0.0.1',
    db='capstone', #데이터베이스 이름
    charset='utf8'
)
cursor = connect_db.cursor()


##### 강남구 업소 추가 #####
with open('./static/map_resources/카카오_강남구.json', encoding='utf-8-sig') as f:
    json_data = json.load(f)

for store in json_data:
    store_name = store["place_name"]
    address = store["address_name"]
    district_name = "강남구"
    category = store["category_name"]

    sql = "INSERT IGNORE INTO `store_info`(store_name, address, district_name, category) VALUES (%s, %s, %s, %s);"
    s = (store_name, address, district_name, category)
    cursor.execute(sql, s)
    connect_db.commit()

f.close()


##### 서초구 업소 추가 #####
with open('./static/map_resources/카카오_서초구.json', encoding='utf-8-sig') as f:
    json_data = json.load(f)

for store in json_data:
    store_name = store["place_name"]
    address = store["address_name"]
    district_name = "서초구"
    category = store["category_name"]

    sql = "INSERT IGNORE INTO `store_info`(store_name, address, district_name, category) VALUES (%s, %s, %s, %s);"
    s = (store_name, address, district_name, category)
    cursor.execute(sql, s)
    connect_db.commit()

f.close()

##### 리뷰 데이터 추가 (우선 임시 테이블 생성 후 전송하였음) #####
df = pd.read_csv('senti_result.csv', names=['store_name', 'pos_rate', 'nag_rate', 'storeTT', 'store_POS', 'store_NAG',
                                            'pos_review', 'nag_review', 'pos_keyword', 'nag_keyword'])


df = df.where((pd.notnull(df)), None)

for index, row in df.iterrows():

    sql = "INSERT IGNORE INTO `kakao_review` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    s = (row.store_name, row.pos_rate, row.nag_rate, row.storeTT, row.store_POS, row.store_NAG,
         row.pos_review, row.nag_review, row.pos_keyword, row.nag_keyword)
    cursor.execute(sql, s)
    connect_db.commit()


##### db 연결 종료 #####
cursor.close()
connect_db.close()