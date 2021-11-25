import nltk
import math
import pandas as pd
from konlpy.tag import Kkma
from konlpy.tag import Okt
from konlpy.corpus import kobill
from konlpy.corpus import kolaw
import matplotlib.pyplot as plt
from wordcloud import WordCloud


review_df= pd.read_csv('./data/테스트2.csv',names=['store_name','review','rank'])
t = Okt()
tokens_ko=[]
store_list =[]

print("================= 가게명 출력 =================")

for k in range(len(review_df)):
    name=review_df['store_name'][k]
    if name not in store_list:
        store_list.append(name)

print(store_list)
print("================= 가게별 텍스트 분류 =================")

vocab_list=[]
for i in store_list:
    tmp_list=[]
    for k in range(len(review_df)):
        test = review_df['review'][k]
        name = review_df['store_name'][k]
        if (str(type(test))=="<class 'str'>")and(i==name):
            tmp_list.append(test)
    vocab_list.append(tmp_list)

print(vocab_list)

##############################
print("================= 가게별 형태소 분석 =================")

morp_list=[]
for k in range(len(vocab_list)):
    tmp_list=[]
    for i in vocab_list[k]:
        tmp_list+=(t.nouns(i))
        #print(i,"\n")
    morp_list.append(tmp_list)
print(morp_list)

print("================= 가게별 wordcloud 만들기 =================")
font_path = 'C:/Users/이유진/AppData/Local/Microsoft/Windows/Fonts/NanumGothic.ttf'
for k in range(len(morp_list)):
    ko=nltk.Text(morp_list[k],name='store_review')
    data= ko.vocab().most_common(15)
    wc = WordCloud(font_path=font_path, relative_scaling=0.2, background_color='white').generate_from_frequencies(dict(data))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

'''for k in range(len(review_df)):
    test=review_df['review'][k]
    #print(type(test))
    if (str(type(test))=="<class 'str'>"):
        morp_list=t.morphs(test)
        for i in morp_list:
            tokens_ko.append(i)
            print(tokens_ko)
            print("====================================")

ko = nltk.Text(tokens_ko, name='test')
data = ko.vocab().most_common(200)
font_path = 'C:/Users/이유진/AppData/Local/Microsoft/Windows/Fonts/NanumGothic.ttf'
wc = WordCloud(font_path=font_path,relative_scaling=0.2,background_color='white').generate_from_frequencies(dict(data))
plt.imshow(wc)
plt.axis('off')
plt.show()'''