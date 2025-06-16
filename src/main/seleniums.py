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

url = 'http://59.23.132.191/30stair/area/area.php?pname=area'
driver.get(url)

# 문제명
title = driver.find_element(By.CLASS_NAME, 'pname').text.strip()

# 제한 시간
time_limit = driver.find_element(By.CLASS_NAME, 'tlimit').text.strip()

# 문제 설명 (첫 번째 <p>)
description = driver.find_element(By.TAG_NAME, 'p').text.strip()

# 입력
input_h4 = driver.find_element(By.XPATH, '/html/body/h4[1]').text.strip()

# 입력 설명 (h4 "입력" 이후 다음 h4 전까지 모든 텍스트)
input_description = driver.execute_script(
    """
    
    const h4s = Array.from(document.querySelectorAll('h4'));
    const inputH4 = h4s.find(h => h.textContent.trim() === '입력');
    if (!inputH4) return '';
    
    const result = [];
    let el = inputH4.nextSibling;

    while (el) {
        if (el.nodeType === Node.ELEMENT_NODE && el.tagName.toLowerCase() === 'h4') break;
        if (el.nodeType === Node.TEXT_NODE && el.textContent.trim()) {
            result.push(el.textContent.trim());
        } else if (el.nodeType === Node.ELEMENT_NODE && el.innerText.trim()) {
            result.push(el.innerText.trim());
        }
        el = el.nextSibling;
    }

    return result.join('\\n').trim();
    
    """
)

# 출력
output_h4 = driver.find_element(By.XPATH, '/html/body/h4[2]').text.strip()

# 출력 설명
output_description = driver.execute_script(
    """
    
    const h4s = Array.from(document.querySelectorAll('h4'));
    const outputH4 = h4s.find(h => h.textContent.trim() === '출력');
    if (!outputH4) return '';
    
    const result = [];
    let el = outputH4.nextSibling;

    while (el) {
        if (el.nodeType === Node.ELEMENT_NODE && el.tagName.toLowerCase() === 'h4') break;
        if (el.nodeType === Node.TEXT_NODE && el.textContent.trim()) {
            result.push(el.textContent.trim());
        } else if (el.nodeType === Node.ELEMENT_NODE && el.innerText.trim()) {
            result.push(el.innerText.trim());
        }
        el = el.nextSibling;
    }

    return result.join('\\n').trim();
    
    """
)

# 입출력 예
sample = driver.find_element(By.CLASS_NAME, 'io').text.strip()

# 출력 확인
print(title)
print(time_limit)
print(description)
print(input_h4)
print(input_description)
print(output_h4)
print(output_description)
print(sample)

driver.quit()
