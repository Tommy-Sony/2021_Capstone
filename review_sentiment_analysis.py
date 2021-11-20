from numpy.core.arrayprint import str_format
import pandas as pd
import re
from konlpy.tag import Okt
from konlpy.tag import Kkma

##### 감성 사전 #####
service_good_feature = {'서비스':['좋','친절','괜찮','최고','빠르','짱','훌륭','추천','감사','구수','최상','대박',
                               '훈훈','특별','개이득','최고','만족','세련','최고','감동'],
                        '사장':['친절','스윗','센스'],
                        '알바':['친절','스윗','센스'],
                        '직원': ['친절','스윗','센스'],
                        '일을':['잘','빠르게'],
                        '일도':['잘','빠르게'],
                        '서빙':['잘','빠르게']}

service_bad_feature = {'서비스': ['아쉽','최악','나쁘','느리','빡치','비추','별로','그냥','낙제','쏘다쏘다','엉망','실망','불친절','문제','컴플레인',
                               '거지','그닥','그다지','구려','불편','엉성','헬','개판'],
                       '알바':['불친절','똑바로','재수'],
                       '사장':['불친절','똑바로','재수'],
                       '직원':['불친절','똑바로','재수'],
                      '일을':['못','느리게','답답'],
                      '일도':['못','느리게', '천천히'],
                      '서빙':['못','느리게','천천히','답답']}

taste_good_feature = {'간':['맞','적절','딱','환상','담백'],
                      '음식':['깔끔'],
                      '맛':['있','좋','나다','최고']}

taste_bad_feature = {'간':['세','쎄','강하다','별로'],
                     '음식':['별로','쏘다쏘다','최악'],
                     '맛':['별로','최악']}

taste_good_emotion = ['고소','부드럽','신선','촉촉','싱싱','정갈','최고']

taste_bad_emotion = ['싱겁','느끼다하다','짜다','느끼다','짜다','딱딱하다','차갑다']

cost_good_feature = {'가격': ['괜찮','착하다','저렴','적당','싸다','좋다','합리적','훌륭','최고','만족','마음','든든','알맞다',
                            '무난','괜춘','최상','최상','굿','엄지','낮'],
                     '가성비':['괜찮','착하다','저렴','적당','싸다','좋다','합리적','훌륭','최고','만족','마음','든든','알맞다',
                            '무난','괜춘','최상','최상','굿','엄지'],
                     '양':['많','적당','푸짐하고','괜찮다','넉넉','충분','든든']
                     }

cost_bad_feature ={'가격': ['비싸','있다','나쁘','사악','비효율','높다','부담','아쉽','쏘다쏘다','별로','그닥','그다지','쎄','ㅎㄷㄷ','높','거품'],
                   '가성비':['별로'],
                   '양':['적다','작다','아쉽','적다','다소','별로'],
                   }

atmosphere_good_feature = {'분위기': ['좋','괜찮','조용','깔끔','적당','깡패','굉장','아담','완벽','아기자기','고급','최고','세련','만족','아늑','훌륭','예쁘','이쁘','짱',
                                   '심쿵','따뜻','깨끗','독특','매력','모던','취향저격','맘','마음','클래식','아름','인상적','귀엽','포근'], 
                           '인테리어': ['좋','괜찮','조용','깔끔','적당','깡패','굉장','아담','완벽','아기자기','고급','최고','세련','만족','아늑','훌륭','예쁘','이쁘','짱',
                                    '심쿵','따뜻','깨끗','독특','매력','모던','취향저격','맘','마음','클래식','아름','인상적','귀엽','포근']}

atmosphere_bad_feature = {'분위기': ['나쁘다','바쁘다','어수선하다','이상하다','촌스럽다','별로','부담스럽다','시끄럽','복잡' ],
                          '인테리어':[]}

visit_good_feature = {'의사':['있다','충만','백프로','백프롭','많','만땅','마구','그득','만점','넘침'],
                      '다시':['가다','오다','방문','찾다','가보다','한번','갈다','찾아가다','가야지','갈거다','방문하다보고',
                            '생각나다','방문한다면','와보고','재방문','접하다','간다면','갈다때가','먹다고프다','방문한다임','오자고','가기로','갈다생각이다','가면'],
                      '굳이':[]}

visit_bad_feature = {'의사':['글쎄'],
                     '굳이':['다시','많이','여기까지','줄서서','찾아','시키다','가다','찾다','여기','기다리다','줄을','사먹'],
                     '다시':[]}

negative_word_emotion = ['안','않','못','없','아닌','아니']


##### 크롤링 데이터 로드 #####
df = pd.read_csv(r'kko_review_text_4.csv', names=['store name', 'review', 'rating'])
okt = Okt()
kkma = Kkma()


##### 전처리 #####
def preprocessing(review):
    review = re.sub('([a-zA-Z])','',review)
    review = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',review)
    review = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]',' ',review)
    review += '. '
    review = okt.normalize(review)
    return review

store_name = []
norm_list = []
for n in df['store name']:
    store_name.append(n)
for s in df['review']:
    norm_list.append(preprocessing(str(s)))


##### 감정 분석 함수 #####
#키워드 추출
def get_feature_keywords(feature_keywords, review):
    feature_temp = []
    for keyword in feature_keywords:
        if re.findall(keyword, review):
            sub_list = ['게','고','음','며','데','만','도','면']
            
            for sub in sub_list:
                if sub+' ' in review:
                    review = re.sub(sub+' ', sub+',', review)

            a = re.findall(keyword +'+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+\s+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+\s+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+',review)
            b = re.findall(keyword + '+\s+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+\s+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+',review)
            c = re.findall('[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+\s+' + keyword +'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+',review)
            d = re.findall(keyword + '[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+\s+[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+',review)

            for ngram in a:
                t = ()
                feature_temp.append(t + (ngram,keyword))
            for ngram in b:
                t = ()
                feature_temp.append(t + (ngram,keyword))
            for ngram in c:
                t = ()
                feature_temp.append(t + (ngram,keyword))
            for ngram in d:

                t = ()
                feature_temp.append(t + (ngram,keyword))

    return feature_temp

#특정 키워드의 감정 추출
def get_feature_emotions(feature_good_dict,feature_bad_dict, feature_temp):
    good_feature_emotion_list = []
    bad_feature_emotion_list = []
    good_feature_keyword_set = set()
    bad_feature_keyword_set = set()

    for ngrams in feature_temp:
        keyword = ngrams[1]
        ngram = ngrams[0]
        is_bad_feature = None

        good_emotion_list = feature_good_dict[keyword]
        bad_emotion_list = feature_bad_dict[keyword]
        for emotion in good_emotion_list:
            if re.findall(emotion, ngram):
                is_bad_feature = False  
        for emotion in bad_emotion_list:
            if re.findall(emotion, ngram):
                is_bad_feature = True    
        for negative in negative_word_emotion:
            if re.findall(negative, ngram):
                if is_bad_feature == True:
                    is_bad_feature = False
                    break
                elif is_bad_feature == False:
                    is_bad_feature = True
                    break
                else:
                    is_bad_feature = True
                    break   
        if is_bad_feature:
            bad_feature_keyword_set.add(keyword)
            bad_feature_emotion_list.append(ngram)
        elif is_bad_feature == False:
            good_feature_keyword_set.add(keyword)
            good_feature_emotion_list.append(ngram)
        else:
            pass
    return good_feature_emotion_list, bad_feature_emotion_list, good_feature_keyword_set, bad_feature_keyword_set

#맛에 대한 감정 추출
def get_taste_emotion(taste_good_emotions, taste_bad_emotions):
    bad_taste_emotion_list = []
    good_taste_emotion_list = []
    for ngrams in taste_good_emotions:
        ngram = ngrams[0]
        is_bad_taste = False
        for negative in negative_word_emotion:
            if re.findall(negative,ngram):
                is_bad_taste = True
        if is_bad_taste:
            bad_taste_emotion_list.append(ngram)
        else:
            good_taste_emotion_list.append(ngram)
    
    for ngrams in taste_bad_emotions:
        ngram = ngrams[0]
        is_bad_taste = True
        for negative in negative_word_emotion:
            if re.findall(negative,ngram):
                is_bad_taste = False
        if is_bad_taste:
            bad_taste_emotion_list.append(ngram)
        else:
            good_taste_emotion_list.append(ngram)
            
    return good_taste_emotion_list, bad_taste_emotion_list


##### 감정 분석 #####
check_division = lambda x, y: y if y ==0 else round((x / float(y)),2)
cnt = 0

for s in norm_list:
    restaurant_good_service_count = 0
    restaurant_bad_service_count = 0
    restaurant_good_atmosphere_count =0
    restaurant_bad_atmosphere_count =0
    restaurant_good_cost_count =0
    restaurant_bad_cost_count =0
    restaurant_good_visit_count = 0
    restaurant_bad_visit_count = 0
    restaurant_good_taste_count = 0
    restaurant_bad_taste_count = 0

    service_temp = get_feature_keywords(service_good_feature.keys(), s)
    good_service, bad_service, good_service_keyword, bad_service_keyword = \
        get_feature_emotions(service_good_feature, service_bad_feature, service_temp)

    atmosphere_temp = get_feature_keywords(atmosphere_good_feature.keys(), s)
    good_atmosphere, bad_atmosphere, good_atmosphere_keyword, bad_atmosphere_keyword = \
        get_feature_emotions(atmosphere_good_feature, atmosphere_bad_feature, atmosphere_temp)

    cost_temp= get_feature_keywords(cost_good_feature.keys(), s)
    good_cost, bad_cost, good_cost_keyword, bad_cost_keyword = \
        get_feature_emotions(cost_good_feature, cost_bad_feature, cost_temp)

    visit_temp = get_feature_keywords(visit_good_feature.keys(), s)
    good_visit, bad_visit, good_visit_keyword, bad_visit_keyword = \
        get_feature_emotions(visit_good_feature, visit_bad_feature, visit_temp)

    taste_temp = get_feature_keywords(taste_good_feature.keys(), s)
    good_taste, bad_taste,  good_taste_keyword, bad_taste_keyword = \
        get_feature_emotions(taste_good_feature, taste_bad_feature, taste_temp)

    taste_good_emotion_temp = get_feature_keywords(taste_good_emotion, s)
    taste_bad_emotion_temp = get_feature_keywords(taste_bad_emotion, s)
    good_taste2, bad_taste2 = get_taste_emotion(taste_good_emotion_temp,taste_bad_emotion_temp)
    good_taste.extend(good_taste2)
    bad_taste.extend(bad_taste2)

    if len(good_service) > len(bad_service):
        restaurant_good_service_count += 1
    elif len(good_service) < len(bad_service):
        restaurant_bad_service_count += 1
    else:
        pass
        
    if len(good_atmosphere) > len(bad_atmosphere):
        restaurant_good_atmosphere_count += 1
    elif len(good_atmosphere) < len(bad_atmosphere):
        restaurant_bad_atmosphere_count += 1
    else:
        pass
        
    if len(good_cost) > len(bad_cost):
        restaurant_good_cost_count += 1
    elif len(good_cost) < len(bad_cost):
        restaurant_bad_cost_count += 1
    else:
        pass
            
    if len(good_visit) > len(bad_visit):
        restaurant_good_visit_count += 1
    elif len(good_visit) < len(bad_visit):
        restaurant_bad_visit_count += 1
    else:
        pass
        
    if len(good_taste) > len(bad_taste):
        restaurant_good_taste_count += 1
    elif len(good_taste) < len(bad_taste):
        restaurant_bad_taste_count += 1
    else:
        pass
        
    TT = restaurant_good_service_count + restaurant_bad_service_count + restaurant_good_taste_count + restaurant_bad_taste_count + restaurant_good_atmosphere_count + restaurant_bad_atmosphere_count + restaurant_good_cost_count + restaurant_bad_cost_count
    good_keywords = set()
    bad_keywords = set()

    g=[]
    b=[]
    if TT > 0:
        print('업소명:', end=' ')
        print(store_name[cnt])
        print('키워드:', end=' ')
        if good_service or bad_service:
            if good_service:
                g+=good_service
                good_keywords.update(good_service_keyword)
            if bad_service:
                b+=bad_service
                bad_keywords.update(bad_service_keyword)
            print(good_service, bad_service)

        if good_atmosphere or bad_atmosphere:
            if good_atmosphere:
                g+=good_atmosphere
                good_keywords.update(good_atmosphere_keyword)
            if bad_service:
                b+=bad_service
                bad_keywords.update(bad_atmosphere_keyword)
            print(good_atmosphere, bad_atmosphere)


        if good_cost or bad_cost:
            if good_atmosphere:
                g+=good_atmosphere
                good_keywords.update(good_cost_keyword)
            if bad_service:
                b+=bad_service
                bad_keywords.update(bad_cost_keyword)
            print(good_cost, bad_cost)

        if good_visit or bad_visit:
            if good_visit:
                g+=good_visit
                #good_keywords.update(good_visit_keyword)
            if bad_visit:
                b+=bad_visit
                #bad_keywords.update(bad_visit_keyword)
            print(good_visit, bad_visit)

        if good_taste or bad_taste:
            if good_taste:
                g+=good_taste
                good_keywords.update(good_taste_keyword)
            if bad_taste:
                b+=bad_taste
                bad_keywords.update(bad_taste_keyword)
            print(good_taste, bad_taste)


        print('Total review count: {}'.format(len(s)))
        print('Good service: {}/{} = {}'.format(restaurant_good_service_count,restaurant_good_service_count + restaurant_bad_service_count,100*check_division(restaurant_good_service_count, restaurant_good_service_count + restaurant_bad_service_count)))
        print('Good atmosphere: {}/{} = {}'.format(restaurant_good_atmosphere_count,restaurant_good_atmosphere_count + restaurant_bad_atmosphere_count,100*check_division(restaurant_good_atmosphere_count,restaurant_good_atmosphere_count + restaurant_bad_atmosphere_count))) 
        print('Good cost: {}/{} = {}'.format(restaurant_good_cost_count,restaurant_good_cost_count + restaurant_bad_cost_count, 100*check_division(restaurant_good_cost_count,restaurant_good_cost_count + restaurant_bad_cost_count)))
        print('Good taste: {}/{} = {}'.format(restaurant_good_taste_count,restaurant_good_taste_count + restaurant_bad_taste_count,100*check_division(restaurant_good_taste_count,restaurant_good_taste_count + restaurant_bad_taste_count)))
        print('')

        gk = []
        bk = []
        gk+=(list(good_keywords))
        bk+=(list(bad_keywords))
        print(gk, bk)

        df2 = pd.DataFrame(
                {
                    'store name': store_name[cnt], \
                    'total': TT, \
                    'good_cnt_all': restaurant_good_service_count + restaurant_good_taste_count + restaurant_good_atmosphere_count + restaurant_good_cost_count, \
                    'bad_cnt_all':restaurant_bad_service_count + restaurant_bad_taste_count + restaurant_bad_atmosphere_count + restaurant_bad_cost_count, \
                    'good_review' : ", ".join(g), \
                    'bad_review' : ", ".join(b), \
                    'good_keyword' : ", ".join(gk), \
                    'bad_keyword' : ", ".join(bk)
                },
                index=[0]
            )
        df2.to_csv(r"senti_analy_list.csv", mode = 'a', header=False, index=False, encoding='utf-8-sig')
    cnt+=1