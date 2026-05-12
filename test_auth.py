import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("测试1: 注册管理员账号")
print("=" * 50)
register_data = {
    "username": "admin",
    "password": "admin123",
    "role": "admin",
    "real_name": "系统管理员",
    "phone": "13800138000"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试2: 注册班主任账号")
print("=" * 50)
register_data2 = {
    "username": "teacher_zhang",
    "password": "teacher123",
    "role": "homeroom",
    "real_name": "张老师",
    "phone": "13800138001"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data2)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试3: 注册任课老师账号")
print("=" * 50)
register_data3 = {
    "username": "teacher_li",
    "password": "teacher456",
    "role": "teacher",
    "real_name": "李老师",
    "phone": "13800138002"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data3)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试4: 登录管理员账号")
print("=" * 50)
login_data = {
    "username": "admin",
    "password": "admin123"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    result = response.json()
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get("code") == 200:
        token = result["data"]["access_token"]
        print("\n" + "=" * 50)
        print("测试5: 获取当前用户信息")
        print("=" * 50)
        response = requests.get(f"{BASE_URL}/api/auth/me", params={"token": token})
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试6: 重复注册（应该失败）")
print("=" * 50)
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试7: 错误密码登录（应该失败）")
print("=" * 50)
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "wrong"})
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"错误: {e}")
