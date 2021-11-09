import pandas as pd
import json

df = pd.read_csv(r'senti_analy_list.csv', names=['store name', 'total', 'good_cnt_all', 'bad_cnt_all', 'good_keyword', 'bad_keyword'])

with open("kakao_search_for_url.json", encoding='UTF-8-sig') as f:
        contents = f.read()
        data = json.loads(contents)

store_name = []
for d in data:
    store_name.append(d['place_name'])

storeTT = 0
store_POS = 0
store_NAG = 0
idx = 0
g = []
b = []

#print(store_name)

i = 0
while i < len(df):
    
    if df['store name'][i] == store_name[idx] :
        storeTT += int(df['total'][i])
        store_POS += int(df['good_cnt_all'][i])
        store_NAG += int(df['bad_cnt_all'][i])
        if (str(df['good_keyword'][i])!='nan'):
            g.append(df['good_keyword'][i])
        if (str(df['bad_keyword'][i])!='nan'):
            b.append(df['bad_keyword'][i])

    else :
        if storeTT > 0:
            for j in range(len(g)):
                g[j]=str(g[j])
            for k in range(len(b)):
                b[k]=str(b[k])
            
            df2 = pd.DataFrame(
                {
                'store name': store_name[idx], \
                'pos rate' : store_POS/storeTT, \
                'nag rate' : store_NAG/storeTT, \
                'storeTT': storeTT, \
                'store POS': store_POS, \
                'store NAG': store_NAG, \
                'pos review': ", ".join(g), \
                'nag review': ", ".join(b)
                },
                index=[0]
            )
            df2.to_csv(r"senti_result.csv", mode = 'a', header=False, index=False, encoding='utf-8-sig')
        
        idx+=1
        i-=1
        storeTT = 0
        store_POS = 0
        store_NAG = 0
        g = []
        b = []
    i+=1