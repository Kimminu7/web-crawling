from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

url = 'http://59.23.132.191/30stair/m2s/m2s.php?pname=m2s'
driver.get(url)

# 문제명
title = driver.find_element(By.CLASS_NAME, 'pname').text.strip()

# 제한 시간
time_limit = driver.find_element(By.CLASS_NAME, 'tlimit').text.strip()

# 문제 설명 (첫 번째 <p>)
description = driver.find_element(By.TAG_NAME, 'p').text.strip()

# 입력 설명
input_h4 = driver.find_element(By.CSS_SELECTOR, 'body > h4:nth-child(4)').text.strip()

# input_description 입력 설명
input_description_elements = driver.find_elements(By.XPATH, '//h4[text()="입력"]/following-sibling::*')
input_description = ""
for el in input_description_elements:
    if el.tag_name.lower() == 'h4':
        break
    input_description += el.text.strip() + "\n"
input_description = input_description.strip()

# 출력 설명
output_h4 = driver.find_element(By.CSS_SELECTOR, 'body > h4:nth-child(6)').text.strip()

# output_description 출력 설명
output_description_elements = driver.find_elements(By.XPATH, '//h4[text()="출력"]/following-sibling::*')
output_description = ""
for el in output_description_elements:
    if el.tag_name.lower() == 'h4':
        break
    output_description += el.text.strip() + "\n"
output_description = output_description.strip()

# 입출력 예
sample = driver.find_element(By.CLASS_NAME, 'io').text.strip()

# 출력 확인
print(title)
print(time_limit)
print(description)
print(input_h4)
# print(input_description)
print(output_h4)
# print(output_description)
print(sample)

driver.quit()
