import requests
import json

#API key 확인
token = 'KakaoAK b9c505bd9c2fe12db14b475cb2992b54'
search_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

#주소 파싱한 파일 open
with open("강남구_모범음식점.json", encoding='utf8') as f:
  contents = f.read()
  data = json.loads(contents)

with open('kakao_search_for_url.json', 'w', encoding='UTF-8-sig') as f:
  f.write('[\n')

#API 호출
for store in data:
  query="?query="
  keyword = store['시군구'] + " " + store['행정동명'] + " " + store['업소명']
  option = ""

  url = search_url + query + keyword
  print(url)
  payload={}
  headers = {
    'Authorization': token
  }
  response = requests.get(url,headers=headers, data=payload)

  result=response.text
  result_json=response.json()
  
  #가게 정보가 있는 곳들만 저장
  if result_json['meta']['pageable_count']>=1:
    with open('kakao_search_for_url.json', 'a', encoding='UTF-8-sig') as json_file:
        json.dump(result_json['documents'][0], json_file, ensure_ascii=False, indent='\t')
        json_file.write('\n,')

#json 파일로 저장
readFile = open("kakao_search_for_url.json", encoding='UTF-8-sig')
lines = readFile.readlines()
readFile.close()

w = open("kakao_search_for_url.json",'w', encoding='UTF-8-sig')
w.writelines([item for item in lines[:-1]])
w.write('\n]')
w.close()