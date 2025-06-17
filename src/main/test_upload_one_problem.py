import json
import requests

# === 설정 ===
API_URL = "http://localhost:8080/api/admin/problems"  # 실제 스프링 서버 주소
HEADERS = {
    "Content-Type": "application/json",
    # 인증이 필요하다면 아래 줄을 주석 해제하고 토큰 입력
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJtaW5qZWVAbmF2ZXIuY29tIiwidXNlcm5hbWUiOiJ0ZXN0bmFtZSIsIm5pY2tuYW1lIjoiTWljayIsInVzZXJSb2xlIjoiQURNSU4iLCJ0aWVyIjoiTkVXQklFIiwiZXhwIjoxNzUwNzUyMDQwLCJpYXQiOjE3NTAxNDcyNDB9.eccdkWJTtSm8_8iuvFrRBiAqMK010OwaM0nF5Heivuc"
}

# === 1개 문제만 로드 ===
with open("formatted_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# 첫 번째 문제만 사용
problem = problems[0]

# === POST 요청 payload 구성 ===
payload = {
    "category": "FOR_BEGINNER",                      # 고정값 또는 조건에 따라 조절
    "title": problem["title"],
    "description": problem["description"],
    "difficulty": "BRONZE",                          # 고정값 또는 조건 분기 가능
    "memoryLimit": 30000,                            # 문제에 따라 조절 가능
    "timeLimit": problem["timeLimit"],       # 문자열이면 float 변환
    "reference": "ORIGINAL"                          # 고정값 또는 "CRAWLED"
}

# === 전송 ===
response = requests.post(API_URL, headers=HEADERS, json=payload)

# === 결과 출력 ===
if response.status_code == 201:
    print(f"✅ 문제 등록 성공: {problem['title']}")
    print("응답 데이터:", response.json())
else:
    print(f"❌ 문제 등록 실패: {problem['title']}")
    print("상태 코드:", response.status_code)
    print("에러 응답:", response.text)
