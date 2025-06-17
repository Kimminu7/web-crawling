from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

# 셀레니움 설정
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 설명 블록 추출 함수 (<h4> 기준)
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

       return result.filter(line => line.trim() !== '').join('\\n').trim();
    """)

# 샘플 input/output 분리 함수
def parse_sample_text(sample_text):
    lines = sample_text.strip().splitlines()
    input_part = []
    output_part = []
    current = None

    for line in lines:
        line = line.strip()
        if line == "입력":
            current = "input"
            continue
        elif line == "출력":
            current = "output"
            continue

        if current == "input":
            input_part.append(line)
        elif current == "output":
            output_part.append(line)
        elif current is None:
            # "입력/출력" 구분 없을 경우 자동 분리
            if not input_part:
                input_part.append(line)
            else:
                output_part.append(line)

    return "\n".join([line for line in input_part if line.strip()]), "\n".join([line for line in output_part if line.strip()])


# 크롤링 시작
base_url = "http://59.23.132.191/30stair/"
results = []

driver.get(base_url)
tables = driver.find_elements(By.XPATH, '/html/body/table')
problem_id = 1

for table_index, table in enumerate(tables, start=1):
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row_index in range(1, len(rows)):
        try:
            xpath = f'/html/body/table[{table_index}]/tbody/tr[{row_index+1}]/td[2]/a'
            link = driver.find_element(By.XPATH, xpath)
            link.click()
            time.sleep(0.5)

            title = driver.find_element(By.XPATH, '/html/body/div[1]').text.strip().replace("프로그램 명: ", "")
            time_limit = driver.find_element(By.XPATH, '/html/body/div[2]').text.strip().replace("제한시간: ", "")

            try:
                description = driver.find_element(By.XPATH, '//*[comment()[contains(., "here")]]/following-sibling::*[1]').text.strip()
            except:
                description = driver.find_element(By.XPATH, '/html/body/p').text.strip()

            input_description = extract_section_text(driver, "입력")
            output_description = extract_section_text(driver, "출력")

            try:
                sample_text = driver.find_element(By.XPATH, '/html/body/pre').text.strip()
            except:
                try:
                    sample_text = driver.find_element(By.CLASS_NAME, 'io').text.strip()
                except:
                    sample_text = ""

            sample_input, sample_output = parse_sample_text(sample_text)

            results.append({
                "id": problem_id,
                "title": title,
                "time_limit": time_limit,
                "description": description,
                "input": input_description,
                "output": output_description,
                "sample_input": sample_input,
                "sample_output": sample_output
            })

            print(f"[{problem_id}] {title} ✅")

        except Exception as e:
            print(f"[{problem_id}] 오류: {e}")

        finally:
            problem_id += 1
            driver.back()
            time.sleep(0.5)

driver.quit()

# JSON 저장
with open("problems.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
