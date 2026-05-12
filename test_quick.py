import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "http://localhost:8000"

def login(u, p):
    r = requests.post(f"{BASE}/api/auth/login", json={"username": u, "password": p})
    if r.status_code == 200:
        return r.json()["data"]["access_token"]
    return None

admin_tok = login("test_admin", "admin123")
home_tok = login("test_homeroom", "home123")
teach_tok = login("test_teacher", "teach123")

print("Tokens:", "admin" if admin_tok else "FAIL", "homeroom" if home_tok else "FAIL", "teacher" if teach_tok else "FAIL")

tests = []

def check(method, url, exp, desc, data=None, headers=None):
    r = requests.request(method, url, json=data, headers=headers, timeout=5)
    ok = r.status_code == exp
    tests.append(ok)
    status = "PASS" if ok else "FAIL"
    print(f"{status} | {desc} | expect={exp} got={r.status_code}")

H_ADMIN = {"Authorization": f"Bearer {admin_tok}"}
H_HOME = {"Authorization": f"Bearer {home_tok}"}
H_TEACH = {"Authorization": f"Bearer {teach_tok}"}

print("\n=== Student Module ===")
check("POST", f"{BASE}/api/students/create", 200, "Admin create student", {"student_no": "T1", "student_name": "T", "gender": "M", "age": 20, "class_id": 1}, H_ADMIN)
check("POST", f"{BASE}/api/students/create", 200, "Homeroom create student", {"student_no": "T2", "student_name": "T", "gender": "F", "age": 21, "class_id": 1}, H_HOME)
check("POST", f"{BASE}/api/students/create", 403, "Teacher create student (deny)", {"student_no": "T3", "student_name": "T", "gender": "M", "age": 22, "class_id": 1}, H_TEACH)

check("PUT", f"{BASE}/api/students/update/1", 200, "Admin update student", {"student_name": "U1"}, H_ADMIN)
check("PUT", f"{BASE}/api/students/update/1", 200, "Homeroom update student", {"student_name": "U2"}, H_HOME)
check("PUT", f"{BASE}/api/students/update/1", 403, "Teacher update student (deny)", {"student_name": "U3"}, H_TEACH)

check("DELETE", f"{BASE}/api/students/delete/1", 200, "Admin delete student", headers=H_ADMIN)
check("DELETE", f"{BASE}/api/students/delete/2", 403, "Homeroom delete student (deny)", headers=H_HOME)
check("DELETE", f"{BASE}/api/students/delete/3", 403, "Teacher delete student (deny)", headers=H_TEACH)

check("PUT", f"{BASE}/api/students/restore/1", 200, "Admin restore student", headers=H_ADMIN)
check("PUT", f"{BASE}/api/students/restore/2", 403, "Homeroom restore student (deny)", headers=H_HOME)
check("PUT", f"{BASE}/api/students/restore/3", 403, "Teacher restore student (deny)", headers=H_TEACH)

print("\n=== Teacher Module ===")
check("POST", f"{BASE}/api/teachers/create", 200, "Admin create teacher", {"teacher_name": "W", "gender": "M", "phone": "13900000001", "subject": "Math"}, H_ADMIN)
check("POST", f"{BASE}/api/teachers/create", 403, "Homeroom create teacher (deny)", {"teacher_name": "Z", "gender": "F", "phone": "13900000002", "subject": "Eng"}, H_HOME)
check("POST", f"{BASE}/api/teachers/create", 403, "Teacher create teacher (deny)", {"teacher_name": "L", "gender": "M", "phone": "13900000003", "subject": "Phy"}, H_TEACH)

check("PUT", f"{BASE}/api/teachers/update/1", 200, "Admin update teacher", {"teacher_name": "WU"}, H_ADMIN)
check("PUT", f"{BASE}/api/teachers/update/1", 403, "Homeroom update teacher (deny)", {"teacher_name": "ZU"}, H_HOME)
check("PUT", f"{BASE}/api/teachers/update/1", 403, "Teacher update teacher (deny)", {"teacher_name": "LU"}, H_TEACH)

check("DELETE", f"{BASE}/api/teachers/delete/1", 200, "Admin delete teacher", headers=H_ADMIN)
check("DELETE", f"{BASE}/api/teachers/delete/2", 403, "Homeroom delete teacher (deny)", headers=H_HOME)
check("DELETE", f"{BASE}/api/teachers/delete/3", 403, "Teacher delete teacher (deny)", headers=H_TEACH)

check("PUT", f"{BASE}/api/teachers/restore/1", 200, "Admin restore teacher", headers=H_ADMIN)
check("PUT", f"{BASE}/api/teachers/restore/2", 403, "Homeroom restore teacher (deny)", headers=H_HOME)
check("PUT", f"{BASE}/api/teachers/restore/3", 403, "Teacher restore teacher (deny)", headers=H_TEACH)

print("\n=== Score Module ===")
check("POST", f"{BASE}/api/scores", 200, "Admin add score", {"student_no": "T1", "subject": "Math", "score": 85.5, "exam_order": 1}, H_ADMIN)
check("POST", f"{BASE}/api/scores", 200, "Homeroom add score", {"student_no": "T1", "subject": "Eng", "score": 90.0, "exam_order": 1}, H_HOME)
check("POST", f"{BASE}/api/scores", 200, "Teacher add score", {"student_no": "T1", "subject": "Phy", "score": 78.5, "exam_order": 1}, H_TEACH)

check("PUT", f"{BASE}/api/scores/1", 200, "Admin update score", {"score": 88.0}, H_ADMIN)
check("PUT", f"{BASE}/api/scores/1", 200, "Homeroom update score", {"score": 92.0}, H_HOME)
check("PUT", f"{BASE}/api/scores/1", 403, "Teacher update score (deny)", {"score": 80.0}, H_TEACH)

check("DELETE", f"{BASE}/api/scores/1", 200, "Admin delete score", headers=H_ADMIN)
check("DELETE", f"{BASE}/api/scores/2", 403, "Homeroom delete score (deny)", headers=H_HOME)
check("DELETE", f"{BASE}/api/scores/3", 403, "Teacher delete score (deny)", headers=H_TEACH)

check("PUT", f"{BASE}/api/scores/delete/restore", 200, "Admin restore score", params={"id": 1}, headers=H_ADMIN)
check("PUT", f"{BASE}/api/scores/delete/restore", 403, "Homeroom restore score (deny)", params={"id": 2}, headers=H_HOME)
check("PUT", f"{BASE}/api/scores/delete/restore", 403, "Teacher restore score (deny)", params={"id": 3}, headers=H_TEACH)

print("\n=== Class Module ===")
check("POST", f"{BASE}/api/classes/add", 200, "Admin create class", {"class_name": "C1", "lecturer_id": 1, "start_date": "2024-09-01"}, H_ADMIN)
check("POST", f"{BASE}/api/classes/add", 403, "Homeroom create class (deny)", {"class_name": "C2", "lecturer_id": 2, "start_date": "2024-09-01"}, H_HOME)
check("POST", f"{BASE}/api/classes/add", 403, "Teacher create class (deny)", {"class_name": "C3", "lecturer_id": 3, "start_date": "2024-09-01"}, H_TEACH)

check("PUT", f"{BASE}/api/classes/update/1", 200, "Admin update class", {"class_name": "CU"}, H_ADMIN)
check("PUT", f"{BASE}/api/classes/update/1", 403, "Homeroom update class (deny)", {"class_name": "CU2"}, H_HOME)
check("PUT", f"{BASE}/api/classes/update/1", 403, "Teacher update class (deny)", {"class_name": "CU3"}, H_TEACH)

check("DELETE", f"{BASE}/api/classes/delete/1", 200, "Admin delete class", headers=H_ADMIN)
check("DELETE", f"{BASE}/api/classes/delete/2", 403, "Homeroom delete class (deny)", headers=H_HOME)
check("DELETE", f"{BASE}/api/classes/delete/3", 403, "Teacher delete class (deny)", headers=H_TEACH)

check("PUT", f"{BASE}/api/classes/restore/1", 200, "Admin restore class", headers=H_ADMIN)
check("PUT", f"{BASE}/api/classes/restore/2", 403, "Homeroom restore class (deny)", headers=H_HOME)
check("PUT", f"{BASE}/api/classes/restore/3", 403, "Teacher restore class (deny)", headers=H_TEACH)

print("\n=== Employment Module ===")
check("POST", f"{BASE}/api/employments/", 200, "Admin create employment", {"student_no": "T1", "company_name": "TX", "position": "Dev", "salary": 15000}, H_ADMIN)
check("POST", f"{BASE}/api/employments/", 200, "Homeroom create employment", {"student_no": "T1", "company_name": "AL", "position": "Test", "salary": 12000}, H_HOME)
check("POST", f"{BASE}/api/employments/", 403, "Teacher create employment (deny)", {"student_no": "T1", "company_name": "BD", "position": "PM", "salary": 13000}, H_TEACH)

check("PUT", f"{BASE}/api/employments/1", 200, "Admin update employment", {"salary": 16000}, H_ADMIN)
check("PUT", f"{BASE}/api/employments/1", 200, "Homeroom update employment", {"salary": 13000}, H_HOME)
check("PUT", f"{BASE}/api/employments/1", 403, "Teacher update employment (deny)", {"salary": 14000}, H_TEACH)

check("DELETE", f"{BASE}/api/employments/1", 200, "Admin delete employment", headers=H_ADMIN)
check("DELETE", f"{BASE}/api/employments/2", 403, "Homeroom delete employment (deny)", headers=H_HOME)
check("DELETE", f"{BASE}/api/employments/3", 403, "Teacher delete employment (deny)", headers=H_TEACH)

check("PUT", f"{BASE}/api/employments/restore/1", 200, "Admin restore employment", headers=H_ADMIN)
check("PUT", f"{BASE}/api/employments/restore/2", 403, "Homeroom restore employment (deny)", headers=H_HOME)
check("PUT", f"{BASE}/api/employments/restore/3", 403, "Teacher restore employment (deny)", headers=H_TEACH)

print("\n=== User Module ===")
check("POST", f"{BASE}/api/auth/register", 200, "Admin register user", {"username": "nu1", "password": "nu123", "role": "teacher", "real_name": "NU1"}, H_ADMIN)
check("POST", f"{BASE}/api/auth/register", 403, "Homeroom register user (deny)", {"username": "nu2", "password": "nu123", "role": "teacher", "real_name": "NU2"}, H_HOME)
check("POST", f"{BASE}/api/auth/register", 403, "Teacher register user (deny)", {"username": "nu3", "password": "nu123", "role": "teacher", "real_name": "NU3"}, H_TEACH)

print(f"\n=== Summary ===")
print(f"PASS: {sum(tests)}")
print(f"FAIL: {len(tests) - sum(tests)}")
print(f"Total: {len(tests)}")
if len(tests) > 0:
    print(f"Rate: {sum(tests)/len(tests)*100:.1f}%")
