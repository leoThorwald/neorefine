#!/usr/bin/env python3
"""Inspect what an endpoint actually returns"""

import requests

endpoint = "/api/peopleType"
base_url = "https://tumoragdb.com.cn"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
}

print(f"Inspecting: {base_url}{endpoint}")
print("-" * 60)

response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type', 'Not specified')}")
print(f"Content-Length: {len(response.content)} bytes")
print()
print("Response content:")
print("-" * 60)
print(response.text[:1000])
print("-" * 60)
