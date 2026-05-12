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

print("="*50)
print("用户认证系统完整测试")
print("="*50)

print_test("注册管理员账号", 1)
data_admin = {"username": "admin_test", "password": "admin123", "role": "admin", "real_name": "测试管理员", "phone": "13800000001"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data_admin)
safe_print_response(resp)

print_test("注册班主任账号", 2)
data_bzr = {"username": "bzr_test", "password": "bzr123", "role": "homeroom", "real_name": "测试班主任", "phone": "13800000002"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data_bzr)
safe_print_response(resp)

print_test("注册任课老师账号", 3)
data_teacher = {"username": "teacher_test", "password": "tch123", "role": "teacher", "real_name": "测试任课老师", "phone": "13800000003"}
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data_teacher)
safe_print_response(resp)

print_test("管理员登录", 4)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin_test", "password": "admin123"})
safe_print_response(resp)
admin_result = resp.json() if resp.status_code == 200 else None

print_test("班主任登录", 5)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "bzr_test", "password": "bzr123"})
safe_print_response(resp)
bzr_result = resp.json() if resp.status_code == 200 else None

print_test("任课老师登录", 6)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "teacher_test", "password": "tch123"})
safe_print_response(resp)
teacher_result = resp.json() if resp.status_code == 200 else None

if admin_result and admin_result["code"] == 200:
    token = admin_result["data"]["access_token"]
    print_test("获取当前用户信息（管理员）", 7)
    resp = requests.get(f"{BASE_URL}/api/auth/me", params={"token": token})
    safe_print_response(resp)

print_test("重复注册（应该失败409）", 8)
resp = requests.post(f"{BASE_URL}/api/auth/register", json=data_admin)
safe_print_response(resp)

print_test("错误密码登录（应该失败401）", 9)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin_test", "password": "wrong"})
safe_print_response(resp)

print_test("不存在的用户登录（应该失败401）", 10)
resp = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "nouser", "password": "test123"})
safe_print_response(resp)

print("\n" + "="*50)
print("所有测试完成！")
print("="*50)
