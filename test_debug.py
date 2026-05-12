import requests
import json

BASE_URL = "http://localhost:8000"

# 测试注册任课老师
print("测试: 注册任课老师账号")
data = {"username": "teacher_test1", "password": "tch456", "role": "teacher", "real_name": "张老师", "phone": "13900139002"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data)
print(f"状态码: {resp.status_code}")
print(f"响应文本: {resp.text}")

# 测试错误密码登录
print("\n测试: 错误密码登录")
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "banzhuren_wang", "password": "wrong"})
print(f"状态码: {resp.status_code}")
print(f"响应文本: {resp.text}")

# 测试不存在的用户
print("\n测试: 不存在的用户登录")
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "nouser123", "password": "test123"})
print(f"状态码: {resp.status_code}")
print(f"响应文本: {resp.text}")
