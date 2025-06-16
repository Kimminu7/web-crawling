from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

# 셀레니움 설정
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 공통 구조에서 <h4> 이후 설명 추출 함수
def extract_section_text(driver, header_text):
    return driver.execute_script(f"""
        const h4s = Array.from(document.querySelectorAll('h4'));
        const header = h4s.find(h => h.textContent.trim() === "{header_text}");
        if (!header) return '';

        const result = [];
        let el = header.nextSibling;

        while (el) {{
            if (el.nodeType === Node.ELEMENT_NODE && el.tagName.toLowerCase() === 'h4') break;
            if (el.nodeType === Node.TEXT_NODE && el.textContent.trim()) {{
                result.push(el.textContent.trim());
            }} else if (el.nodeType === Node.ELEMENT_NODE && el.innerText.trim()) {{
                result.push(el.innerText.trim());
            }}
            el = el.nextSibling;
        }}

        return result.join('\\n').trim();
    """)

# 문제 ID 리스트 (10개)
problem_ids = [
    "area", "m2s", "swap", "op", "triangle", "average", "CtoF", "q_r", "change", "sec", "k"
]

base_url = "http://59.23.132.191/30stair/"
results = []

driver.get(base_url)
for i in range(3, 10):
    try:
        driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr['+str(i)+']/td[2]/a').click()
        time.sleep(0.1)
        title = driver.find_element(By.XPATH, '/html/body/div[1]').text.strip().replace("프로그램 명: ", "")
        time_limit = driver.find_element(By.XPATH, '/html/body/div[2]').text.strip().replace("제한시간: ", "")
        try:
            description = driver.find_element(By.XPATH, '//*[comment()[contains(., "here")]]/following-sibling::*[1]').text.strip()
        except:
            description = driver.find_element(By.XPATH, '/html/body/p').text.strip()
        input_description = extract_section_text(driver, "입력")
        output_description = extract_section_text(driver, "출력")

        try:
            sample = driver.find_element(By.XPATH, '/html/body/pre').text.strip()
        except:
            sample = ""

        results.append({
            "id": i,
            "title": title,
            "time_limit": time_limit,
            "description": description,
            "input": input_description,
            "output": output_description,
            "sample": sample
        })

    except Exception as e:
        try:
            sample = driver.find_element(By.CLASS_NAME, 'io').text.strip()
        except:
            sample = ""
        results.append({
            "id": i,
            "error": str(e)
        })
    driver.back()
driver.quit()

# JSON 저장
with open("problems.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
