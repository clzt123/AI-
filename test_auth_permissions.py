import requests
import json

BASE_URL = "http://localhost:8000"

PASS = "✓"
FAIL = "✗"

def test_api(method, url, expected_status, description, json_data=None, headers=None, params=None):
    try:
        response = requests.request(method, url, json=json_data, headers=headers, params=params)
        status = PASS if response.status_code == expected_status else FAIL
        print(f"{status} {description}")
        print(f"  期望状态码: {expected_status}, 实际: {response.status_code}")
        if response.status_code != expected_status:
            print(f"  响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"✗ {description}")
        print(f"  错误: {e}")
        return False

def login(username, password):
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        data = response.json()
        return data["data"]["access_token"]
    return None

print("=" * 60)
print("初始化测试：注册管理员账号（无需鉴权）")
print("=" * 60)
admin_register = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "test_admin",
    "password": "admin123",
    "role": "admin",
    "real_name": "测试管理员",
    "phone": "13800000001"
})
print(f"注册管理员: {admin_register.status_code}")

print("\n" + "=" * 60)
print("获取管理员Token")
print("=" * 60)
admin_token = login("test_admin", "admin123")
admin_headers = {"Authorization": f"Bearer {admin_token}"}
print(f"管理员Token: {'获取成功' if admin_token else '获取失败'}")

print("\n" + "=" * 60)
print("通过管理员创建班主任和任课老师账号")
print("=" * 60)
homeroom_reg = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "test_homeroom",
    "password": "home123",
    "role": "homeroom",
    "real_name": "测试班主任",
    "phone": "13800000002"
}, headers=admin_headers)
print(f"注册班主任: {homeroom_reg.status_code}")

teacher_reg = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "test_teacher",
    "password": "teach123",
    "role": "teacher",
    "real_name": "测试任课老师",
    "phone": "13800000003"
}, headers=admin_headers)
print(f"注册任课老师: {teacher_reg.status_code}")

print("\n" + "=" * 60)
print("获取各角色Token")
print("=" * 60)
homeroom_token = login("test_homeroom", "home123")
teacher_token = login("test_teacher", "teach123")

homeroom_headers = {"Authorization": f"Bearer {homeroom_token}"}
teacher_headers = {"Authorization": f"Bearer {teacher_token}"}

print(f"班主任Token: {'获取成功' if homeroom_token else '获取失败'}")
print(f"任课老师Token: {'获取成功' if teacher_token else '获取失败'}")

results = {"pass": 0, "fail": 0}

def run_test(method, url, expected_status, description, json_data=None, headers=None, params=None):
    success = test_api(method, url, expected_status, description, json_data, headers, params)
    if success:
        results["pass"] += 1
    else:
        results["fail"] += 1

print("\n" + "=" * 60)
print("1. 学生管理模块鉴权测试")
print("=" * 60)

print("\n创建学生 (admin, homeroom 允许; teacher 拒绝)")
run_test("POST", f"{BASE_URL}/api/students/create", 200, "管理员创建学生", 
         json_data={"student_no": "S001", "student_name": "测试学生", "gender": "男", "age": 20, "class_id": 1}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/students/create", 200, "班主任创建学生", 
         json_data={"student_no": "S002", "student_name": "测试学生2", "gender": "女", "age": 21, "class_id": 1}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/students/create", 403, "任课老师创建学生(应拒绝)", 
         json_data={"student_no": "S003", "student_name": "测试学生3", "gender": "男", "age": 22, "class_id": 1}, 
         headers=teacher_headers)

print("\n更新学生 (admin, homeroom 允许; teacher 拒绝)")
run_test("PUT", f"{BASE_URL}/api/students/update/1", 200, "管理员更新学生", 
         json_data={"student_name": "更新学生"}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/students/update/1", 200, "班主任更新学生", 
         json_data={"student_name": "更新学生2"}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/students/update/1", 403, "任课老师更新学生(应拒绝)", 
         json_data={"student_name": "更新学生3"}, 
         headers=teacher_headers)

print("\n删除学生 (仅admin允许)")
run_test("DELETE", f"{BASE_URL}/api/students/delete/1", 200, "管理员删除学生", 
         headers=admin_headers)
run_test("DELETE", f"{BASE_URL}/api/students/delete/2", 403, "班主任删除学生(应拒绝)", 
         headers=homeroom_headers)
run_test("DELETE", f"{BASE_URL}/api/students/delete/3", 403, "任课老师删除学生(应拒绝)", 
         headers=teacher_headers)

print("\n恢复学生 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/students/restore/1", 200, "管理员恢复学生", 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/students/restore/2", 403, "班主任恢复学生(应拒绝)", 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/students/restore/3", 403, "任课老师恢复学生(应拒绝)", 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("2. 老师管理模块鉴权测试")
print("=" * 60)

print("\n创建老师 (仅admin允许)")
run_test("POST", f"{BASE_URL}/api/teachers/create", 200, "管理员创建老师", 
         json_data={"teacher_name": "王老师", "gender": "男", "phone": "13900000001", "subject": "数学"}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/teachers/create", 403, "班主任创建老师(应拒绝)", 
         json_data={"teacher_name": "赵老师", "gender": "女", "phone": "13900000002", "subject": "英语"}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/teachers/create", 403, "任课老师创建老师(应拒绝)", 
         json_data={"teacher_name": "刘老师", "gender": "男", "phone": "13900000003", "subject": "物理"}, 
         headers=teacher_headers)

print("\n更新老师 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/teachers/update/1", 200, "管理员更新老师", 
         json_data={"teacher_name": "更新王老师"}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/teachers/update/1", 403, "班主任更新老师(应拒绝)", 
         json_data={"teacher_name": "更新赵老师"}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/teachers/update/1", 403, "任课老师更新老师(应拒绝)", 
         json_data={"teacher_name": "更新刘老师"}, 
         headers=teacher_headers)

print("\n删除老师 (仅admin允许)")
run_test("DELETE", f"{BASE_URL}/api/teachers/delete/1", 200, "管理员删除老师", 
         headers=admin_headers)
run_test("DELETE", f"{BASE_URL}/api/teachers/delete/2", 403, "班主任删除老师(应拒绝)", 
         headers=homeroom_headers)
run_test("DELETE", f"{BASE_URL}/api/teachers/delete/3", 403, "任课老师删除老师(应拒绝)", 
         headers=teacher_headers)

print("\n恢复老师 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/teachers/restore/1", 200, "管理员恢复老师", 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/teachers/restore/2", 403, "班主任恢复老师(应拒绝)", 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/teachers/restore/3", 403, "任课老师恢复老师(应拒绝)", 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("3. 成绩管理模块鉴权测试")
print("=" * 60)

print("\n添加成绩 (admin, homeroom, teacher 均允许)")
run_test("POST", f"{BASE_URL}/api/scores", 200, "管理员添加成绩", 
         json_data={"student_no": "S001", "subject": "数学", "score": 85.5, "exam_order": 1}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/scores", 200, "班主任添加成绩", 
         json_data={"student_no": "S001", "subject": "英语", "score": 90.0, "exam_order": 1}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/scores", 200, "任课老师添加成绩", 
         json_data={"student_no": "S001", "subject": "物理", "score": 78.5, "exam_order": 1}, 
         headers=teacher_headers)

print("\n更新成绩 (admin, homeroom 允许; teacher 拒绝)")
run_test("PUT", f"{BASE_URL}/api/scores/1", 200, "管理员更新成绩", 
         json_data={"score": 88.0}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/scores/1", 200, "班主任更新成绩", 
         json_data={"score": 92.0}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/scores/1", 403, "任课老师更新成绩(应拒绝)", 
         json_data={"score": 80.0}, 
         headers=teacher_headers)

print("\n删除成绩 (仅admin允许)")
run_test("DELETE", f"{BASE_URL}/api/scores/1", 200, "管理员删除成绩", 
         headers=admin_headers)
run_test("DELETE", f"{BASE_URL}/api/scores/2", 403, "班主任删除成绩(应拒绝)", 
         headers=homeroom_headers)
run_test("DELETE", f"{BASE_URL}/api/scores/3", 403, "任课老师删除成绩(应拒绝)", 
         headers=teacher_headers)

print("\n恢复成绩 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/scores/delete/restore", 200, "管理员恢复成绩", 
         params={"id": 1}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/scores/delete/restore", 403, "班主任恢复成绩(应拒绝)", 
         params={"id": 2}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/scores/delete/restore", 403, "任课老师恢复成绩(应拒绝)", 
         params={"id": 3}, 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("4. 班级管理模块鉴权测试")
print("=" * 60)

print("\n创建班级 (仅admin允许)")
run_test("POST", f"{BASE_URL}/api/classes/add", 200, "管理员创建班级", 
         json_data={"class_name": "2024级1班", "lecturer_id": 1, "start_date": "2024-09-01"}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/classes/add", 403, "班主任创建班级(应拒绝)", 
         json_data={"class_name": "2024级2班", "lecturer_id": 2, "start_date": "2024-09-01"}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/classes/add", 403, "任课老师创建班级(应拒绝)", 
         json_data={"class_name": "2024级3班", "lecturer_id": 3, "start_date": "2024-09-01"}, 
         headers=teacher_headers)

print("\n更新班级 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/classes/update/1", 200, "管理员更新班级", 
         json_data={"class_name": "更新班级"}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/classes/update/1", 403, "班主任更新班级(应拒绝)", 
         json_data={"class_name": "更新班级2"}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/classes/update/1", 403, "任课老师更新班级(应拒绝)", 
         json_data={"class_name": "更新班级3"}, 
         headers=teacher_headers)

print("\n删除班级 (仅admin允许)")
run_test("DELETE", f"{BASE_URL}/api/classes/delete/1", 200, "管理员删除班级", 
         headers=admin_headers)
run_test("DELETE", f"{BASE_URL}/api/classes/delete/2", 403, "班主任删除班级(应拒绝)", 
         headers=homeroom_headers)
run_test("DELETE", f"{BASE_URL}/api/classes/delete/3", 403, "任课老师删除班级(应拒绝)", 
         headers=teacher_headers)

print("\n恢复班级 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/classes/restore/1", 200, "管理员恢复班级", 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/classes/restore/2", 403, "班主任恢复班级(应拒绝)", 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/classes/restore/3", 403, "任课老师恢复班级(应拒绝)", 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("5. 就业管理模块鉴权测试")
print("=" * 60)

print("\n创建就业信息 (admin, homeroom 允许; teacher 拒绝)")
run_test("POST", f"{BASE_URL}/api/employments/", 200, "管理员创建就业信息", 
         json_data={"student_no": "S001", "company_name": "腾讯", "position": "开发", "salary": 15000}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/employments/", 200, "班主任创建就业信息", 
         json_data={"student_no": "S002", "company_name": "阿里", "position": "测试", "salary": 12000}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/employments/", 403, "任课老师创建就业信息(应拒绝)", 
         json_data={"student_no": "S003", "company_name": "百度", "position": "产品", "salary": 13000}, 
         headers=teacher_headers)

print("\n更新就业信息 (admin, homeroom 允许; teacher 拒绝)")
run_test("PUT", f"{BASE_URL}/api/employments/1", 200, "管理员更新就业信息", 
         json_data={"salary": 16000}, 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/employments/1", 200, "班主任更新就业信息", 
         json_data={"salary": 13000}, 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/employments/1", 403, "任课老师更新就业信息(应拒绝)", 
         json_data={"salary": 14000}, 
         headers=teacher_headers)

print("\n删除就业信息 (仅admin允许)")
run_test("DELETE", f"{BASE_URL}/api/employments/1", 200, "管理员删除就业信息", 
         headers=admin_headers)
run_test("DELETE", f"{BASE_URL}/api/employments/2", 403, "班主任删除就业信息(应拒绝)", 
         headers=homeroom_headers)
run_test("DELETE", f"{BASE_URL}/api/employments/3", 403, "任课老师删除就业信息(应拒绝)", 
         headers=teacher_headers)

print("\n恢复就业信息 (仅admin允许)")
run_test("PUT", f"{BASE_URL}/api/employments/restore/1", 200, "管理员恢复就业信息", 
         headers=admin_headers)
run_test("PUT", f"{BASE_URL}/api/employments/restore/2", 403, "班主任恢复就业信息(应拒绝)", 
         headers=homeroom_headers)
run_test("PUT", f"{BASE_URL}/api/employments/restore/3", 403, "任课老师恢复就业信息(应拒绝)", 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("6. 用户管理模块鉴权测试")
print("=" * 60)

print("\n注册用户 (仅admin允许)")
run_test("POST", f"{BASE_URL}/api/auth/register", 200, "管理员注册用户", 
         json_data={"username": "new_user", "password": "new123", "role": "teacher", "real_name": "新用户"}, 
         headers=admin_headers)
run_test("POST", f"{BASE_URL}/api/auth/register", 403, "班主任注册用户(应拒绝)", 
         json_data={"username": "new_user2", "password": "new123", "role": "teacher", "real_name": "新用户2"}, 
         headers=homeroom_headers)
run_test("POST", f"{BASE_URL}/api/auth/register", 403, "任课老师注册用户(应拒绝)", 
         json_data={"username": "new_user3", "password": "new123", "role": "teacher", "real_name": "新用户3"}, 
         headers=teacher_headers)

print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
print(f"通过: {results['pass']}")
print(f"失败: {results['fail']}")
print(f"总计: {results['pass'] + results['fail']}")
print(f"通过率: {results['pass'] / (results['pass'] + results['fail']) * 100:.1f}%")
