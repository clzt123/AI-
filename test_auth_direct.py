import requests
import sys
import os

# Set encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://localhost:8000"

def login(u, p):
    try:
        r = requests.post(f"{BASE}/api/auth/login", json={"username": u, "password": p}, timeout=5)
        if r.status_code == 200:
            return r.json()["data"]["access_token"]
    except Exception as e:
        print(f"Login error: {e}")
    return None

def test(method, url, expected, desc, data=None, headers=None, params=None):
    try:
        r = requests.request(method, url, json=data, headers=headers, params=params, timeout=5)
        ok = r.status_code == expected
        status = "PASS" if ok else "FAIL"
        msg = f"{status} | {desc} | expect={expected} got={r.status_code}"
        print(msg)
        if not ok:
            print(f"       Response: {r.text[:100]}")
        return ok
    except Exception as e:
        print(f"ERROR | {desc} | {e}")
        return False

print("Logging in...")
admin_tok = login("admin", "admin123")
print(f"Admin login: {'OK' if admin_tok else 'FAIL'}")

if not admin_tok:
    print("Creating admin user...")
    r = requests.post(f"{BASE}/api/auth/register", json={"username": "admin", "password": "admin123", "role": "admin", "real_name": "Admin"}, timeout=5)
    print(f"Register: {r.status_code} - {r.text[:100]}")
    admin_tok = login("admin", "admin123")
    print(f"Admin login after register: {'OK' if admin_tok else 'FAIL'}")

if not admin_tok:
    print("Cannot proceed without admin token")
    sys.exit(1)

H_A = {"Authorization": f"Bearer {admin_tok}"}

# Create test users
print("\nCreating test users...")
r = requests.post(f"{BASE}/api/auth/register", json={"username": "test_homeroom", "password": "home123", "role": "homeroom", "real_name": "Homeroom"}, headers=H_A, timeout=5)
print(f"Create homeroom: {r.status_code}")

r = requests.post(f"{BASE}/api/auth/register", json={"username": "test_teacher", "password": "teach123", "role": "teacher", "real_name": "Teacher"}, headers=H_A, timeout=5)
print(f"Create teacher: {r.status_code}")

home_tok = login("test_homeroom", "home123")
teach_tok = login("test_teacher", "teach123")

print(f"Homeroom login: {'OK' if home_tok else 'FAIL'}")
print(f"Teacher login: {'OK' if teach_tok else 'FAIL'}")

if not all([admin_tok, home_tok, teach_tok]):
    print("Failed to get all tokens")
    sys.exit(1)

H_H = {"Authorization": f"Bearer {home_tok}"}
H_T = {"Authorization": f"Bearer {teach_tok}"}

passed = 0
failed = 0

print("\n=== Student Module ===")
if test("PUT", f"{BASE}/api/students/update/1", 200, "Admin update", {"student_name": "U"}, H_A): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/students/update/1", 200, "Homeroom update", {"student_name": "U"}, H_H): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/students/update/1", 403, "Teacher update (deny)", {"student_name": "U"}, H_T): passed += 1
else: failed += 1

if test("DELETE", f"{BASE}/api/students/delete/1", 200, "Admin delete", headers=H_A): passed += 1
else: failed += 1

if test("DELETE", f"{BASE}/api/students/delete/1", 403, "Homeroom delete (deny)", headers=H_H): passed += 1
else: failed += 1

if test("DELETE", f"{BASE}/api/students/delete/1", 403, "Teacher delete (deny)", headers=H_T): passed += 1
else: failed += 1

print("\n=== Teacher Module ===")
if test("PUT", f"{BASE}/api/teachers/update/1", 200, "Admin update", {"teacher_name": "WU"}, H_A): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/teachers/update/1", 403, "Homeroom update (deny)", {"teacher_name": "ZU"}, H_H): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/teachers/update/1", 403, "Teacher update (deny)", {"teacher_name": "LU"}, H_T): passed += 1
else: failed += 1

print("\n=== Score Module ===")
if test("PUT", f"{BASE}/api/scores/1", 200, "Admin update", {"score": 88.0}, H_A): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/scores/1", 200, "Homeroom update", {"score": 92.0}, H_H): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/scores/1", 403, "Teacher update (deny)", {"score": 80.0}, H_T): passed += 1
else: failed += 1

print("\n=== Class Module ===")
if test("PUT", f"{BASE}/api/classes/update/1", 200, "Admin update", {"class_name": "CU"}, H_A): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/classes/update/1", 403, "Homeroom update (deny)", {"class_name": "CU2"}, H_H): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/classes/update/1", 403, "Teacher update (deny)", {"class_name": "CU3"}, H_T): passed += 1
else: failed += 1

print("\n=== Employment Module ===")
if test("PUT", f"{BASE}/api/employments/1", 200, "Admin update", {"salary": 16000}, H_A): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/employments/1", 200, "Homeroom update", {"salary": 13000}, H_H): passed += 1
else: failed += 1

if test("PUT", f"{BASE}/api/employments/1", 403, "Teacher update (deny)", {"salary": 14000}, H_T): passed += 1
else: failed += 1

print("\n=== User Module ===")
if test("POST", f"{BASE}/api/auth/register", 200, "Admin register", {"username": "auth200", "password": "auth123", "role": "teacher", "real_name": "Auth1"}, H_A): passed += 1
else: failed += 1

if test("POST", f"{BASE}/api/auth/register", 403, "Homeroom register (deny)", {"username": "auth201", "password": "auth123", "role": "teacher", "real_name": "Auth2"}, H_H): passed += 1
else: failed += 1

if test("POST", f"{BASE}/api/auth/register", 403, "Teacher register (deny)", {"username": "auth202", "password": "auth123", "role": "teacher", "real_name": "Auth3"}, H_T): passed += 1
else: failed += 1

total = passed + failed
print(f"\n=== Summary ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total: {total}")
if total > 0:
    print(f"Pass rate: {passed/total*100:.1f}%")
