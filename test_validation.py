import requests
import json

BASE_URL = "http://localhost:8000"

def test(name, data, expected_status):
    print(f"\n测试: {name}")
    print(f"数据: {json.dumps(data, ensure_ascii=False)}")
    resp = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"状态码: {resp.status_code} (期望: {expected_status})")
    try:
        print(f"响应: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应文本: {resp.text}")
    status = "PASS" if resp.status_code == expected_status else "FAIL"
    print(f"结果: {status}")
    return resp.status_code == expected_status

results = []

results.append(test("正常注册", {
    "username": "testuser_valid",
    "password": "pass123",
    "role": "admin",
    "real_name": "测试用户",
    "phone": "13800138000"
}, 200))

results.append(test("用户名太短", {
    "username": "ab",
    "password": "pass123",
    "role": "admin"
}, 422))

results.append(test("密码太短", {
    "username": "testuser_short",
    "password": "abc",
    "role": "admin"
}, 422))

results.append(test("密码无数字", {
    "username": "testuser_no_num",
    "password": "abcdef",
    "role": "admin"
}, 422))

results.append(test("密码无字母", {
    "username": "testuser_no_char",
    "password": "123456",
    "role": "admin"
}, 422))

results.append(test("无效角色", {
    "username": "testuser_role",
    "password": "pass123",
    "role": "invalid_role"
}, 422))

results.append(test("无效手机号", {
    "username": "testuser_phone",
    "password": "pass123",
    "role": "admin",
    "phone": "12345678901"
}, 422))

results.append(test("有效手机号", {
    "username": "testuser_phone2",
    "password": "pass123",
    "role": "admin",
    "phone": "13800138001"
}, 200))

print("\n" + "="*50)
print(f"测试完成: {sum(results)}/{len(results)} 通过")
print("="*50)
