import requests
BASE = "http://localhost:8000"

def login(u, p):
    r = requests.post(f"{BASE}/api/auth/login", json={"username": u, "password": p})
    if r.status_code == 200:
        return r.json()["data"]["access_token"]
    return None

admin_tok = login("test_admin", "admin123")
home_tok = login("test_homeroom", "home123")
teach_tok = login("test_teacher", "teach123")

print(f"Admin token: {'OK' if admin_tok else 'FAIL'}")
print(f"Homeroom token: {'OK' if home_tok else 'FAIL'}")
print(f"Teacher token: {'OK' if teach_tok else 'FAIL'}")

H_A = {"Authorization": f"Bearer {admin_tok}"}
H_H = {"Authorization": f"Bearer {home_tok}"}
H_T = {"Authorization": f"Bearer {teach_tok}"}

passed = 0
failed = 0

def test(method, url, expected, desc, data=None, headers=None, params=None):
    global passed, failed
    try:
        r = requests.request(method, url, json=data, headers=headers, params=params, timeout=5)
        ok = r.status_code == expected
        if ok:
            passed += 1
            print(f"PASS: {desc}")
        else:
            failed += 1
            print(f"FAIL: {desc} - expected {expected}, got {r.status_code}")
            print(f"  Response: {r.text[:150]}")
    except Exception as e:
        failed += 1
        print(f"ERROR: {desc} - {e}")

print("\n=== Student Module ===")
test("POST", f"{BASE}/api/students/create", 200, "Admin create", {"student_no": "T1", "student_name": "T", "gender": "M", "age": 20, "class_id": 1}, H_A)
test("POST", f"{BASE}/api/students/create", 200, "Homeroom create", {"student_no": "T2", "student_name": "T", "gender": "F", "age": 21, "class_id": 1}, H_H)
test("POST", f"{BASE}/api/students/create", 403, "Teacher create (deny)", {"student_no": "T3", "student_name": "T", "gender": "M", "age": 22, "class_id": 1}, H_T)

test("PUT", f"{BASE}/api/students/update/1", 200, "Admin update", {"student_name": "U"}, H_A)
test("PUT", f"{BASE}/api/students/update/1", 200, "Homeroom update", {"student_name": "U"}, H_H)
test("PUT", f"{BASE}/api/students/update/1", 403, "Teacher update (deny)", {"student_name": "U"}, H_T)

test("DELETE", f"{BASE}/api/students/delete/1", 200, "Admin delete", headers=H_A)
test("DELETE", f"{BASE}/api/students/delete/2", 403, "Homeroom delete (deny)", headers=H_H)
test("DELETE", f"{BASE}/api/students/delete/3", 403, "Teacher delete (deny)", headers=H_T)

test("PUT", f"{BASE}/api/students/restore/1", 200, "Admin restore", headers=H_A)
test("PUT", f"{BASE}/api/students/restore/2", 403, "Homeroom restore (deny)", headers=H_H)
test("PUT", f"{BASE}/api/students/restore/3", 403, "Teacher restore (deny)", headers=H_T)

print("\n=== Teacher Module ===")
test("POST", f"{BASE}/api/teachers/create", 200, "Admin create", {"teacher_name": "W", "gender": "M", "phone": "13900000001", "subject": "Math"}, H_A)
test("POST", f"{BASE}/api/teachers/create", 403, "Homeroom create (deny)", {"teacher_name": "Z", "gender": "F", "phone": "13900000002", "subject": "Eng"}, H_H)
test("POST", f"{BASE}/api/teachers/create", 403, "Teacher create (deny)", {"teacher_name": "L", "gender": "M", "phone": "13900000003", "subject": "Phy"}, H_T)

test("PUT", f"{BASE}/api/teachers/update/1", 200, "Admin update", {"teacher_name": "WU"}, H_A)
test("PUT", f"{BASE}/api/teachers/update/1", 403, "Homeroom update (deny)", {"teacher_name": "ZU"}, H_H)
test("PUT", f"{BASE}/api/teachers/update/1", 403, "Teacher update (deny)", {"teacher_name": "LU"}, H_T)

test("DELETE", f"{BASE}/api/teachers/delete/1", 200, "Admin delete", headers=H_A)
test("DELETE", f"{BASE}/api/teachers/delete/2", 403, "Homeroom delete (deny)", headers=H_H)
test("DELETE", f"{BASE}/api/teachers/delete/3", 403, "Teacher delete (deny)", headers=H_T)

test("PUT", f"{BASE}/api/teachers/restore/1", 200, "Admin restore", headers=H_A)
test("PUT", f"{BASE}/api/teachers/restore/2", 403, "Homeroom restore (deny)", headers=H_H)
test("PUT", f"{BASE}/api/teachers/restore/3", 403, "Teacher restore (deny)", headers=H_T)

print("\n=== Score Module ===")
test("POST", f"{BASE}/api/scores", 200, "Admin add", {"student_no": "T1", "subject": "Math", "score": 85.5, "exam_order": 1}, H_A)
test("POST", f"{BASE}/api/scores", 200, "Homeroom add", {"student_no": "T1", "subject": "Eng", "score": 90.0, "exam_order": 1}, H_H)
test("POST", f"{BASE}/api/scores", 200, "Teacher add", {"student_no": "T1", "subject": "Phy", "score": 78.5, "exam_order": 1}, H_T)

test("PUT", f"{BASE}/api/scores/1", 200, "Admin update", {"score": 88.0}, H_A)
test("PUT", f"{BASE}/api/scores/1", 200, "Homeroom update", {"score": 92.0}, H_H)
test("PUT", f"{BASE}/api/scores/1", 403, "Teacher update (deny)", {"score": 80.0}, H_T)

test("DELETE", f"{BASE}/api/scores/1", 200, "Admin delete", headers=H_A)
test("DELETE", f"{BASE}/api/scores/2", 403, "Homeroom delete (deny)", headers=H_H)
test("DELETE", f"{BASE}/api/scores/3", 403, "Teacher delete (deny)", headers=H_T)

test("PUT", f"{BASE}/api/scores/delete/restore", 200, "Admin restore", params={"id": 1}, headers=H_A)
test("PUT", f"{BASE}/api/scores/delete/restore", 403, "Homeroom restore (deny)", params={"id": 2}, headers=H_H)
test("PUT", f"{BASE}/api/scores/delete/restore", 403, "Teacher restore (deny)", params={"id": 3}, headers=H_T)

print("\n=== Class Module ===")
test("POST", f"{BASE}/api/classes/add", 200, "Admin create", {"class_name": "C1", "lecturer_id": 1, "start_date": "2024-09-01"}, H_A)
test("POST", f"{BASE}/api/classes/add", 403, "Homeroom create (deny)", {"class_name": "C2", "lecturer_id": 2, "start_date": "2024-09-01"}, H_H)
test("POST", f"{BASE}/api/classes/add", 403, "Teacher create (deny)", {"class_name": "C3", "lecturer_id": 3, "start_date": "2024-09-01"}, H_T)

test("PUT", f"{BASE}/api/classes/update/1", 200, "Admin update", {"class_name": "CU"}, H_A)
test("PUT", f"{BASE}/api/classes/update/1", 403, "Homeroom update (deny)", {"class_name": "CU2"}, H_H)
test("PUT", f"{BASE}/api/classes/update/1", 403, "Teacher update (deny)", {"class_name": "CU3"}, H_T)

test("DELETE", f"{BASE}/api/classes/delete/1", 200, "Admin delete", headers=H_A)
test("DELETE", f"{BASE}/api/classes/delete/2", 403, "Homeroom delete (deny)", headers=H_H)
test("DELETE", f"{BASE}/api/classes/delete/3", 403, "Teacher delete (deny)", headers=H_T)

test("PUT", f"{BASE}/api/classes/restore/1", 200, "Admin restore", headers=H_A)
test("PUT", f"{BASE}/api/classes/restore/2", 403, "Homeroom restore (deny)", headers=H_H)
test("PUT", f"{BASE}/api/classes/restore/3", 403, "Teacher restore (deny)", headers=H_T)

print("\n=== Employment Module ===")
test("POST", f"{BASE}/api/employments/", 200, "Admin create", {"student_no": "T1", "company_name": "TX", "position": "Dev", "salary": 15000}, H_A)
test("POST", f"{BASE}/api/employments/", 200, "Homeroom create", {"student_no": "T1", "company_name": "AL", "position": "Test", "salary": 12000}, H_H)
test("POST", f"{BASE}/api/employments/", 403, "Teacher create (deny)", {"student_no": "T1", "company_name": "BD", "position": "PM", "salary": 13000}, H_T)

test("PUT", f"{BASE}/api/employments/1", 200, "Admin update", {"salary": 16000}, H_A)
test("PUT", f"{BASE}/api/employments/1", 200, "Homeroom update", {"salary": 13000}, H_H)
test("PUT", f"{BASE}/api/employments/1", 403, "Teacher update (deny)", {"salary": 14000}, H_T)

test("DELETE", f"{BASE}/api/employments/1", 200, "Admin delete", headers=H_A)
test("DELETE", f"{BASE}/api/employments/2", 403, "Homeroom delete (deny)", headers=H_H)
test("DELETE", f"{BASE}/api/employments/3", 403, "Teacher delete (deny)", headers=H_T)

test("PUT", f"{BASE}/api/employments/restore/1", 200, "Admin restore", headers=H_A)
test("PUT", f"{BASE}/api/employments/restore/2", 403, "Homeroom restore (deny)", headers=H_H)
test("PUT", f"{BASE}/api/employments/restore/3", 403, "Teacher restore (deny)", headers=H_T)

print("\n=== User Module ===")
test("POST", f"{BASE}/api/auth/register", 200, "Admin register", {"username": "nu1", "password": "nu123", "role": "teacher", "real_name": "NU1"}, H_A)
test("POST", f"{BASE}/api/auth/register", 403, "Homeroom register (deny)", {"username": "nu2", "password": "nu123", "role": "teacher", "real_name": "NU2"}, H_H)
test("POST", f"{BASE}/api/auth/register", 403, "Teacher register (deny)", {"username": "nu3", "password": "nu123", "role": "teacher", "real_name": "NU3"}, H_T)

print(f"\n=== Summary ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total: {passed + failed}")
if passed + failed > 0:
    print(f"Pass rate: {passed/(passed+failed)*100:.1f}%")
