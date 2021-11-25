import pandas as pd
from konlpy.tag import Okt
import numpy as np
train_df= pd.read_csv('./data/강남구_크롤링.csv',names=['store_name','review','rank'])
test_df= pd.read_csv('./data/서초구_크롤링.csv',names=['store_name','review','rank'])

okt=Okt()

def tokenize(doc):
    #형태소와 품사를 join
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

train_df.isnull().any() #document에 null값이 있다.
train_df['review'] = train_df['review'].fillna(''); #null값을 ''값으로 대체

test_df.isnull().any()
test_df['review'] = test_df['review'].fillna(''); #null값을 ''값으로 대체

#print(train_df.values)
train_docs = [(tokenize(row[1]), row[2]) for row in train_df.values]
test_docs = [(tokenize(row[1]), row[2]) for row in test_df.values]

tokens = [t for d in train_docs for t in d[0]]
print("토큰개수:", len(tokens))

import nltk
text = nltk.Text(tokens, name='NMSC')

#토큰개수
print(len(text.tokens))

#중복을 제외한 토큰개수
print(len(set(text.tokens)))

#출력빈도가 높은 상위 토큰 10개
print(text.vocab().most_common(10))

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
plt.figure(figsize=(20,10))
plt.rc('font', family='NanumGothic')
text.plot(50)

FREQUENCY_COUNT = 100;
selected_words = [f[0] for f in text.vocab().most_common(FREQUENCY_COUNT)]

#단어리스트 문서에서 상위 10000개들중 포함되는 단어들이 개수
def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

#문서에 들어가는 단어 개수
x_train = [term_frequency(d) for d,_ in train_docs]
x_test = [term_frequency(d) for d,_ in test_docs]

#라벨(1 or 0)
y_train = [c for _,c in train_docs]
y_test = [c for _,c in test_docs]

x_train = np.asarray(x_train).astype('float32')
x_test = np.asarray(x_test).astype('float32')

y_train = np.asarray(y_train).astype('float32')
y_test = np.asarray(y_test).astype('float32')

import tensorflow as tf

#레이어 구성
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(FREQUENCY_COUNT,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

#학습 프로세스 설정
model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.001),
    loss=tf.keras.losses.binary_crossentropy,
    metrics=[tf.keras.metrics.binary_accuracy]
    )

#학습 데이터로 학습
model.fit(x_train, y_train, epochs=10, batch_size=512)

results = model.evaluate(x_test, y_test)
print(results)

#모델을 저장해둘수도 있다.
model.save('movie_review_model.h5')