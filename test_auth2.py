import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("测试1: 注册新用户 testuser1")
print("=" * 50)
register_data = {
    "username": "testuser1",
    "password": "test123",
    "role": "admin",
    "real_name": "测试用户1",
    "phone": "13900139000"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"状态码: {response.status_code}")
    print(f"响应文本: {response.text}")
    if response.status_code == 200:
        result = response.json()
        print(f"响应JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"异常: {e}")
    print(f"响应状态码: {response.status_code if 'response' in locals() else 'N/A'}")
    print(f"响应文本: {response.text if 'response' in locals() else 'N/A'}")

print("\n" + "=" * 50)
print("测试2: 登录新用户")
print("=" * 50)
login_data = {
    "username": "testuser1",
    "password": "test123"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"状态码: {response.status_code}")
    print(f"响应文本: {response.text}")
    if response.status_code == 200:
        result = response.json()
        print(f"响应JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"异常: {e}")
