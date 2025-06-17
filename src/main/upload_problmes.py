import json
import requests

# JSON 파일 경로
with open("problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# Spring API 서버 주소
URL = "http://localhost:8080/api/admin/problems"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # 인증 필요 시만
}

# 문제 하나씩 등록
for p in problems:
    try:
        payload = {
            "category": "FOR_BEGINNER",              # 필요 시 수정
            "title": p["title"],
            "description": p["description"],
            "difficulty": "BRONZE",                  # 필요 시 수정
            "memoryLimit": 30000,
            "timeLimit": float(p["time_limit"]),     # 문자열일 경우 float 변환
            "reference": "ORIGINAL"
        }

        res = requests.post(URL, headers=HEADERS, json=payload)
        print(f"{p['title']} 등록 상태: {res.status_code}")

        if res.status_code >= 400:
            print("에러 응답:", res.text)

    except Exception as e:
        print(f"문제 등록 중 예외 발생: {e}")
