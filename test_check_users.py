import requests
import sys

BASE = "http://localhost:8000"

# First try to login with default admin
print("Trying to login with admin/admin123...")
try:
    r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"}, timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
    if r.status_code == 200:
        tok = r.json()["data"]["access_token"]
        print(f"Token: {tok[:50]}...")
except Exception as e:
    print(f"Error: {e}")

# Try to register a test admin
print("\nTrying to register test users...")
try:
    # First create admin user
    r = requests.post(f"{BASE}/api/auth/register", json={"username": "test_admin", "password": "admin123", "role": "admin", "real_name": "TestAdmin"}, timeout=5)
    print(f"Register admin: {r.status_code} - {r.text[:100]}")
except Exception as e:
    print(f"Error: {e}")
