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

base_url = "http://59.23.132.191/30stair/"
results = []

driver.get(base_url)
tables = driver.find_elements(By.XPATH, '/html/body/table')
problem_id = 1

for table_index, table in enumerate(tables, start=1):
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # 실제 문제 데이터는 보통 tr[2]부터 시작 (헤더 제외)
    for row_index in range(1, len(rows)):
        try:
            # 동적으로 table과 row 인덱스 조합
            xpath = f'/html/body/table[{table_index}]/tbody/tr[{row_index+1}]/td[2]/a'
            link = driver.find_element(By.XPATH, xpath)
            link.click()
            time.sleep(0.002)

            # 문제 상세 수집
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
                try:
                    sample = driver.find_element(By.CLASS_NAME, 'io').text.strip()
                except:
                    sample = ""

            results.append({
                "id": problem_id,
                "title": title,
                "time_limit": time_limit,
                "description": description,
                "input": input_description,
                "output": output_description,
                "sample": sample
            })
            print(f"[{problem_id}] {title} ✅")

        except Exception as e:
            print(f"[{problem_id}] 오류: {e}")

        finally:
            problem_id += 1
            driver.back()
            time.sleep(0.002)

driver.quit()

# JSON 저장
with open("problems.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


