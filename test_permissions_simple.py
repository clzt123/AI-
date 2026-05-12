import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

def login(username, password):
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    return None

admin_token = login("test_admin", "admin123")
homeroom_token = login("test_homeroom", "home123")
teacher_token = login("test_teacher", "teach123")

admin_headers = {"Authorization": f"Bearer {admin_token}"}
homeroom_headers = {"Authorization": f"Bearer {homeroom_token}"}
teacher_headers = {"Authorization": f"Bearer {teacher_token}"}

pass_count = 0
fail_count = 0

def test(method, url, expected, desc, data=None, headers=None, params=None):
    global pass_count, fail_count
    try:
        r = requests.request(method, url, json=data, headers=headers, params=params, timeout=5)
        ok = r.status_code == expected
        symbol = "✓" if ok else "✗"
        print(f"{symbol} {desc}")
        if not ok:
            print(f"  期望:{expected} 实际:{r.status_code} 响应:{r.text[:100]}")
        if ok:
            pass_count += 1
        else:
            fail_count += 1
    except Exception as e:
        print(f"✗ {desc}")
        print(f"  错误:{e}")
        fail_count += 1

print("=" * 60)
print("1. 学生管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/students/create", 200, "管理员创建学生", 
     {"student_no": "TS001", "student_name": "测试1", "gender": "男", "age": 20, "class_id": 1}, admin_headers)
test("POST", f"{BASE_URL}/api/students/create", 200, "班主任创建学生", 
     {"student_no": "TS002", "student_name": "测试2", "gender": "女", "age": 21, "class_id": 1}, homeroom_headers)
test("POST", f"{BASE_URL}/api/students/create", 403, "任课老师创建学生(应拒绝)", 
     {"student_no": "TS003", "student_name": "测试3", "gender": "男", "age": 22, "class_id": 1}, teacher_headers)

test("PUT", f"{BASE_URL}/api/students/update/1", 200, "管理员更新学生", 
     {"student_name": "更新1"}, admin_headers)
test("PUT", f"{BASE_URL}/api/students/update/1", 200, "班主任更新学生", 
     {"student_name": "更新2"}, homeroom_headers)
test("PUT", f"{BASE_URL}/api/students/update/1", 403, "任课老师更新学生(应拒绝)", 
     {"student_name": "更新3"}, teacher_headers)

test("DELETE", f"{BASE_URL}/api/students/delete/1", 200, "管理员删除学生", headers=admin_headers)
test("DELETE", f"{BASE_URL}/api/students/delete/2", 403, "班主任删除学生(应拒绝)", headers=homeroom_headers)
test("DELETE", f"{BASE_URL}/api/students/delete/3", 403, "任课老师删除学生(应拒绝)", headers=teacher_headers)

test("PUT", f"{BASE_URL}/api/students/restore/1", 200, "管理员恢复学生", headers=admin_headers)
test("PUT", f"{BASE_URL}/api/students/restore/2", 403, "班主任恢复学生(应拒绝)", headers=homeroom_headers)
test("PUT", f"{BASE_URL}/api/students/restore/3", 403, "任课老师恢复学生(应拒绝)", headers=teacher_headers)

print("\n" + "=" * 60)
print("2. 老师管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/teachers/create", 200, "管理员创建老师", 
     {"teacher_name": "王老师", "gender": "男", "phone": "13900000001", "subject": "数学"}, admin_headers)
test("POST", f"{BASE_URL}/api/teachers/create", 403, "班主任创建老师(应拒绝)", 
     {"teacher_name": "赵老师", "gender": "女", "phone": "13900000002", "subject": "英语"}, homeroom_headers)
test("POST", f"{BASE_URL}/api/teachers/create", 403, "任课老师创建老师(应拒绝)", 
     {"teacher_name": "刘老师", "gender": "男", "phone": "13900000003", "subject": "物理"}, teacher_headers)

test("PUT", f"{BASE_URL}/api/teachers/update/1", 200, "管理员更新老师", 
     {"teacher_name": "更新王老师"}, admin_headers)
test("PUT", f"{BASE_URL}/api/teachers/update/1", 403, "班主任更新老师(应拒绝)", 
     {"teacher_name": "更新赵老师"}, homeroom_headers)
test("PUT", f"{BASE_URL}/api/teachers/update/1", 403, "任课老师更新老师(应拒绝)", 
     {"teacher_name": "更新刘老师"}, teacher_headers)

test("DELETE", f"{BASE_URL}/api/teachers/delete/1", 200, "管理员删除老师", headers=admin_headers)
test("DELETE", f"{BASE_URL}/api/teachers/delete/2", 403, "班主任删除老师(应拒绝)", headers=homeroom_headers)
test("DELETE", f"{BASE_URL}/api/teachers/delete/3", 403, "任课老师删除老师(应拒绝)", headers=teacher_headers)

test("PUT", f"{BASE_URL}/api/teachers/restore/1", 200, "管理员恢复老师", headers=admin_headers)
test("PUT", f"{BASE_URL}/api/teachers/restore/2", 403, "班主任恢复老师(应拒绝)", headers=homeroom_headers)
test("PUT", f"{BASE_URL}/api/teachers/restore/3", 403, "任课老师恢复老师(应拒绝)", headers=teacher_headers)

print("\n" + "=" * 60)
print("3. 成绩管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/scores", 200, "管理员添加成绩", 
     {"student_no": "TS001", "subject": "数学", "score": 85.5, "exam_order": 1}, admin_headers)
test("POST", f"{BASE_URL}/api/scores", 200, "班主任添加成绩", 
     {"student_no": "TS001", "subject": "英语", "score": 90.0, "exam_order": 1}, homeroom_headers)
test("POST", f"{BASE_URL}/api/scores", 200, "任课老师添加成绩", 
     {"student_no": "TS001", "subject": "物理", "score": 78.5, "exam_order": 1}, teacher_headers)

test("PUT", f"{BASE_URL}/api/scores/1", 200, "管理员更新成绩", 
     {"score": 88.0}, admin_headers)
test("PUT", f"{BASE_URL}/api/scores/1", 200, "班主任更新成绩", 
     {"score": 92.0}, homeroom_headers)
test("PUT", f"{BASE_URL}/api/scores/1", 403, "任课老师更新成绩(应拒绝)", 
     {"score": 80.0}, teacher_headers)

test("DELETE", f"{BASE_URL}/api/scores/1", 200, "管理员删除成绩", headers=admin_headers)
test("DELETE", f"{BASE_URL}/api/scores/2", 403, "班主任删除成绩(应拒绝)", headers=homeroom_headers)
test("DELETE", f"{BASE_URL}/api/scores/3", 403, "任课老师删除成绩(应拒绝)", headers=teacher_headers)

test("PUT", f"{BASE_URL}/api/scores/delete/restore", 200, "管理员恢复成绩", 
     params={"id": 1}, headers=admin_headers)
test("PUT", f"{BASE_URL}/api/scores/delete/restore", 403, "班主任恢复成绩(应拒绝)", 
     params={"id": 2}, headers=homeroom_headers)
test("PUT", f"{BASE_URL}/api/scores/delete/restore", 403, "任课老师恢复成绩(应拒绝)", 
     params={"id": 3}, headers=teacher_headers)

print("\n" + "=" * 60)
print("4. 班级管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/classes/add", 200, "管理员创建班级", 
     {"class_name": "测试班1", "lecturer_id": 1, "start_date": "2024-09-01"}, admin_headers)
test("POST", f"{BASE_URL}/api/classes/add", 403, "班主任创建班级(应拒绝)", 
     {"class_name": "测试班2", "lecturer_id": 2, "start_date": "2024-09-01"}, homeroom_headers)
test("POST", f"{BASE_URL}/api/classes/add", 403, "任课老师创建班级(应拒绝)", 
     {"class_name": "测试班3", "lecturer_id": 3, "start_date": "2024-09-01"}, teacher_headers)

test("PUT", f"{BASE_URL}/api/classes/update/1", 200, "管理员更新班级", 
     {"class_name": "更新班级"}, admin_headers)
test("PUT", f"{BASE_URL}/api/classes/update/1", 403, "班主任更新班级(应拒绝)", 
     {"class_name": "更新班级2"}, homeroom_headers)
test("PUT", f"{BASE_URL}/api/classes/update/1", 403, "任课老师更新班级(应拒绝)", 
     {"class_name": "更新班级3"}, teacher_headers)

test("DELETE", f"{BASE_URL}/api/classes/delete/1", 200, "管理员删除班级", headers=admin_headers)
test("DELETE", f"{BASE_URL}/api/classes/delete/2", 403, "班主任删除班级(应拒绝)", headers=homeroom_headers)
test("DELETE", f"{BASE_URL}/api/classes/delete/3", 403, "任课老师删除班级(应拒绝)", headers=teacher_headers)

test("PUT", f"{BASE_URL}/api/classes/restore/1", 200, "管理员恢复班级", headers=admin_headers)
test("PUT", f"{BASE_URL}/api/classes/restore/2", 403, "班主任恢复班级(应拒绝)", headers=homeroom_headers)
test("PUT", f"{BASE_URL}/api/classes/restore/3", 403, "任课老师恢复班级(应拒绝)", headers=teacher_headers)

print("\n" + "=" * 60)
print("5. 就业管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/employments/", 200, "管理员创建就业信息", 
     {"student_no": "TS001", "company_name": "腾讯", "position": "开发", "salary": 15000}, admin_headers)
test("POST", f"{BASE_URL}/api/employments/", 200, "班主任创建就业信息", 
     {"student_no": "TS001", "company_name": "阿里", "position": "测试", "salary": 12000}, homeroom_headers)
test("POST", f"{BASE_URL}/api/employments/", 403, "任课老师创建就业信息(应拒绝)", 
     {"student_no": "TS001", "company_name": "百度", "position": "产品", "salary": 13000}, teacher_headers)

test("PUT", f"{BASE_URL}/api/employments/1", 200, "管理员更新就业信息", 
     {"salary": 16000}, admin_headers)
test("PUT", f"{BASE_URL}/api/employments/1", 200, "班主任更新就业信息", 
     {"salary": 13000}, homeroom_headers)
test("PUT", f"{BASE_URL}/api/employments/1", 403, "任课老师更新就业信息(应拒绝)", 
     {"salary": 14000}, teacher_headers)

test("DELETE", f"{BASE_URL}/api/employments/1", 200, "管理员删除就业信息", headers=admin_headers)
test("DELETE", f"{BASE_URL}/api/employments/2", 403, "班主任删除就业信息(应拒绝)", headers=homeroom_headers)
test("DELETE", f"{BASE_URL}/api/employments/3", 403, "任课老师删除就业信息(应拒绝)", headers=teacher_headers)

test("PUT", f"{BASE_URL}/api/employments/restore/1", 200, "管理员恢复就业信息", headers=admin_headers)
test("PUT", f"{BASE_URL}/api/employments/restore/2", 403, "班主任恢复就业信息(应拒绝)", headers=homeroom_headers)
test("PUT", f"{BASE_URL}/api/employments/restore/3", 403, "任课老师恢复就业信息(应拒绝)", headers=teacher_headers)

print("\n" + "=" * 60)
print("6. 用户管理模块")
print("=" * 60)

test("POST", f"{BASE_URL}/api/auth/register", 200, "管理员注册用户", 
     {"username": "new_user1", "password": "new123", "role": "teacher", "real_name": "新用户1"}, admin_headers)
test("POST", f"{BASE_URL}/api/auth/register", 403, "班主任注册用户(应拒绝)", 
     {"username": "new_user2", "password": "new123", "role": "teacher", "real_name": "新用户2"}, homeroom_headers)
test("POST", f"{BASE_URL}/api/auth/register", 403, "任课老师注册用户(应拒绝)", 
     {"username": "new_user3", "password": "new123", "role": "teacher", "real_name": "新用户3"}, teacher_headers)

print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
print(f"✓ 通过: {pass_count}")
print(f"✗ 失败: {fail_count}")
print(f"总计: {pass_count + fail_count}")
if pass_count + fail_count > 0:
    print(f"通过率: {pass_count / (pass_count + fail_count) * 100:.1f}%")
