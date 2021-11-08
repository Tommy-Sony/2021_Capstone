import os
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

import pandas as pd
import csv

# 작업 디렉터리에 chromedriver 있는지 확인!
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기

def main():
    global driver, load_wb, review_num

    driver.implicitly_wait(4)  #렌더링 4초 대기

    # Kakao_api_search.py 로부터의 출력 파일 open > URL 받아오기
    with open("kakao_search_for_url.json", encoding='UTF-8-sig') as f:
        contents = f.read()
        data = json.loads(contents)

    #페이지 지정
    for d in data:
        #검색할 목록
        driver.get(d['place_url'])
        extract_review(d['place_name'])

        idx=3
        try:
            page_num = len(driver.find_elements_by_class_name('link_page')) #페이지 수 찾기
            for i in range(page_num-1):
            #css selector를 이용해 페이지 버튼 누르기
                driver.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(idx) +')').send_keys(Keys.ENTER)
                sleep(1)
                extract_review(d['place_name'])
                idx += 1
            driver.find_element_by_link_text('다음').send_keys(Keys.ENTER) #5페이지가 넘는 경우 다음 버튼 누르기
            sleep(1)
            extract_review(d['place_name']) #리뷰 추출
        except (NoSuchElementException, ElementNotInteractableException):
            print("no review in crawling")

        #그 이후 페이지
        while True:
            idx = 4
            try:
                page_num = len(driver.find_elements_by_class_name('link_page'))
                for i in range(page_num-1):
                    driver.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(idx) +')').send_keys(Keys.ENTER)
                    sleep(1)
                    extract_review(d['place_name'])
                    idx += 1
                driver.find_element_by_link_text('다음').send_keys(Keys.ENTER) #10페이지 이상으로 넘어가기 위한 다음 버튼 클릭
                sleep(1)
                extract_review(d['place_name']) #리뷰 추출
            except (NoSuchElementException, ElementNotInteractableException):
                print("no review in crawling")
                break 
    
    driver.quit()
    print("finish")


def extract_review(place_name):
    global driver
    
    ret = True
    #driver.find_element_by_xpath('//*[@id="mArticle"]/div[5]/div[3]/ul')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')

    #리뷰가 있는 경우
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            #더보기가 있는 리뷰들의 경우 펼쳐야 하는데, 제대로 작동하지 않음.. 
            #driver.find_element_by_css_selector("#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child(5) > div.comment_info > p > button").click()
            comment = review.select('.txt_comment > span') #리뷰
            rating = review.select('.grade_star > em') #별점
            val = ''
            if len(comment) != 0:
                if len(rating) != 0:
                    val = comment[0].text + '/' + rating[0].text.replace('점', '')
                else:
                    val = comment[0].text + '/0'
                print(val) #확인용 출력
                df2 = pd.DataFrame(
                    #저장할 정보 (변경 가능)
                    {
                    'store name': place_name, \
                    'review': comment[0].text, \
                    'rating': rating[0].text
                    },
                    index=[0]
                )

                #csv 파일로 저장
                df2.to_csv(r"kko_review.csv", mode = 'a', header=False, index=False, encoding='utf-8-sig')

    else:
        print('no review in extract')
        ret = False

    return ret


if __name__ == "__main__":
    main()
