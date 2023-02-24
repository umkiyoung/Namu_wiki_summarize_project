from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from Model import model_load
from Model import preprocessing
from Model import summarizing
import sys


def chromeWebDriver():
    chrome_service  = ChromeService(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = chrome_service, options = options)
    return driver

def document_not_found(driver):
    if driver.find_element(By.TAG_NAME, 'p').text == "해당 문서를 찾을 수 없습니다.":
        print("실제 나무위키에 등록된 이름으로 검색해야 합니다.")
        driver.close()
        sys.exit()
        sys.exit("종료")

def textRetrieval(name):
    driver = chromeWebDriver()
    driver.get('https://namu.wiki/w/' + name)
    document_not_found(driver)
    driver.implicitly_wait(2)
    driver.maximize_window()
    index_list = driver.find_element(By.CLASS_NAME, '_0yPpiNcJ').text.split('\n') #목차
    text_list= driver.find_elements(By.CLASS_NAME, 'qp2Iq0Hi') #내용
    text_list = [i.text for i in text_list]
    driver.close()

    index_text = {}
    for i in range(len(index_list)):
        index_text[index_list[i]] = text_list[i]

    return index_list, text_list, index_text #목차와 그에 상응하는 텍스트값 리스트 및 딕셔너리 형태로 반환


def run_separate(name, model, tokenizer):
    index_list, text_list, index_text = textRetrieval(name)
    print(index_list)
    choose = input("요약을 원하는 인덱스 번호를 입력 >> EX) '1.' '3.2.' ")

    for i in range(len(index_list)):
        if index_list[i].startswith(choose, ):
            key = index_list[i]
            print('선택한 목차 >> ',index_list[i])
            break
    text = index_text[key]
    text = preprocessing(text)
    print(f"원본문서 >> \n{text}")
    #요약
    summarized = summarizing(text, model, tokenizer)
    print(f"요약 결과 >> \n{summarized}")

def run_totally(name, model, tokenizer):
    index_list, text_list, index_text = textRetrieval(name)
    for i in range(len(index_list)):
        print(index_list[i],summarizing(preprocessing(text_list[i]),model,tokenizer),sep='\n')


if __name__ == '__main__':
    name = '김유경                                                                                                     '
    model, tokenizer = model_load('gogamza')
    #run_separate(name, model, tokenizer)
    run_totally(name,model,tokenizer)







