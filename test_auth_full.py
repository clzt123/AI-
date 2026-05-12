import requests
import json

BASE_URL = "http://localhost:8000"

def print_test(name, num):
    print(f"\n{'='*50}")
    print(f"测试{num}: {name}")
    print(f"{'='*50}")

def safe_print_response(resp):
    print(f"状态码: {resp.status_code}")
    try:
        print(f"响应: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应文本: {resp.text}")

print_test("注册班主任账号", 1)
data1 = {"username": "banzhuren_wang", "password": "bzr123", "role": "homeroom", "real_name": "王老师", "phone": "13900139001"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data1)
safe_print_response(resp)

print_test("注册任课老师账号", 2)
data2 = {"username": "teacher_zhang", "password": "tch456", "role": "teacher", "real_name": "张老师", "phone": "13900139002"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data2)
safe_print_response(resp)

print_test("班主任登录", 3)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "banzhuren_wang", "password": "bzr123"})
safe_print_response(resp)
result = resp.json() if resp.status_code == 200 else None

print_test("任课老师登录", 4)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "teacher_zhang", "password": "tch456"})
safe_print_response(resp)
result = resp.json() if resp.status_code == 200 else None

if result and result["code"] == 200:
    token = result["data"]["access_token"]
    print_test("获取当前用户信息", 5)
    resp = requests.get(f"{BASE_URL}/api/auth/me", params={"token": token})
    safe_print_response(resp)

print_test("重复注册（应该失败409）", 6)
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data1)
safe_print_response(resp)

print_test("错误密码登录（应该失败401）", 7)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "banzhuren_wang", "password": "wrong"})
safe_print_response(resp)

print_test("不存在的用户登录（应该失败401）", 8)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "nouser", "password": "test123"})
safe_print_response(resp)

print("\n" + "="*50)
print("所有测试完成！")
print("="*50)
