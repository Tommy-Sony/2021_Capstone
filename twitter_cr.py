from time import sleep
import twitter
import pandas as pd
import csv
import datetime
import json

###################################################################################
# 행정구역별 음식점 목록을 받아와, 트위터에 검색한 결과를 JSON 파일로 반환하는 코드입니다
# 현재 지원 행정구역: 서초구

# INPUT: 작업 디렉토리 / Pandas이용한 csv파일처리.html 로부터의 csv 파일 (서초구음식점.csv)
# OUTPUT: 작업 디렉토리 / result.csv 파일 및 result.json 파일

# 추가해야 할 기능
# -다른 행정구역(구체적으로 어떻게 할지?)
# -따옴표로 묶어서 쿼리 던지는 방법(이스케이프 이슈)

###################################################################################


##### 트위터 API 정보 #####
twitter_consumer_key = "6yGOK78IMiiZHpS5UuDgRj4Eo"
twitter_consumer_secret = "w1viRlvhP7jtVAvNp1bXRZnMHHL4CSBdTaFrz3BigMNMqQklPE"  
twitter_access_token = "1433691358603079685-mBertU74SJymJhQVGK0WXatiYSaXcp"
twitter_access_secret = "ljeVTw69Sz92OKbmTHVFeLMWGqdGs5T9qOS29UWU9zfNc"
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret, 
                          access_token_key=twitter_access_token, 
                          access_token_secret=twitter_access_secret)


##### 음식점 리스트 csv 파일에서 업소명 읽어옴 #####
f = open('서초구음식점.csv', 'r', encoding='cp949')
district_name = "서초"
reader = csv.DictReader(f)
store_name = []

#업소명을 list로 저장
for row in reader:
    store_name.append(row.get('업소명'))

f.close()

##### 크롤링 파트 #####
count = 0
for n in store_name:

    #쿼리문 작성
    query = district_name + n 
    filter = "-filter:retweets"
    filter_keyword = " -유흥 -출장"

    query = query + filter + filter_keyword #큰따옴표 이스케이프가 안됩니다 여러분,,할복하겟습니다


    #API 메소드 호출(15분당 180번 제한)
    statuses = twitter_api.GetSearch(term=query, count=10)
    count+=1
    print(n)

    for status in statuses:
        df2 = pd.DataFrame(
            #저장할 정보 (변경 가능)
            {
            'store name': [n], \
            'user name': [status.user.name], \
            'user id': [status.user.id], \
            'tweet': [status.text], \
            'rt count': [status.retweet_count], \
            'fav count': [status.favorite_count], \
            'tweet date': [status.created_at]
            }
        )

        print(df2)
        #csv 파일로 저장
        df2.to_csv(r"result.csv", mode = 'a', header=False, index=False, encoding='utf-8-sig')

        #rate limit 방지
    if count >= 179:
        print(datetime.datetime.now())
        count = 0
        sleep(901)


##### CSV 파일을 JSON 파일로 변환 #####
try:
    df = pd.read_csv (r'result.csv', names=['store name', 'user name', 'user id', 'tweet', 'rt count', 'fav count', 'tweet date'])
    df.to_json (r'result.json', force_ascii=False)
except FileNotFoundError:
    print("검색 결과 없음")
    pass

