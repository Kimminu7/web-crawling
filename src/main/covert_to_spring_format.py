import json

# 원본 문제 JSON 파일 열기
with open("problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# 변환된 문제 리스트와 테스트케이스 맵 준비
formatted_problems = []
testcase_map = {}

for p in problems:
    formatted_problems.append({
        "category": "FOR_BEGINNER",
        "title": p["title"],
        "description": p["description"],
        "difficulty": "BRONZE",
        "memoryLimit": 50000,
        "timeLimit": p["time_limit"],
        "reference": "ORIGINAL"
    })

    title = p["title"]
    testcase_map[title] = []

    if p.get("sample_input", "").strip() and p.get("sample_output", "").strip():
        testcase_map[title].append({
            "input": p["sample_input"].strip(),
            "output": p["sample_output"].strip()
        })

# 결과 저장
with open("formatted_problems.json", "w", encoding="utf-8") as f:
    json.dump(formatted_problems, f, indent=2, ensure_ascii=False)

with open("formatted_testcases.json", "w", encoding="utf-8") as f:
    json.dump(testcase_map, f, indent=2, ensure_ascii=False)
