#!/usr/bin/env python3
"""
Quick API Endpoint Tester
Test a specific endpoint to see if it works before running the full scraper
"""

import sys
import requests
import json

if len(sys.argv) < 2:
    print("Usage: python3 test_endpoint.py <endpoint>")
    print("Example: python3 test_endpoint.py /api/search")
    sys.exit(1)

endpoint = sys.argv[1]
base_url = "https://tumoragdb.com.cn"

print(f"Testing endpoint: {endpoint}")
print(f"Full URL: {base_url}{endpoint}")
print("-" * 60)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
}

# Try different parameter combinations
test_params = [
    {"page": 1, "size": 10},
    {"page": 1, "pageSize": 10},
    {"pageNum": 1, "pageSize": 10},
    {"current": 1, "pageSize": 10},
    {"offset": 0, "limit": 10},
    {},  # No params
]

success = False

for i, params in enumerate(test_params, 1):
    print(f"\n[Test {i}] Trying params: {params}")

    try:
        response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS! Got JSON response")
                print(f"Response type: {type(data)}")

                # Analyze structure
                if isinstance(data, dict):
                    print(f"Response keys: {list(data.keys())}")

                    # Look for data array
                    for key in ['data', 'records', 'items', 'results', 'list']:
                        if key in data:
                            print(f"Found '{key}' key:")
                            item = data[key]
                            if isinstance(item, list):
                                print(f"  - Type: list with {len(item)} items")
                                if len(item) > 0:
                                    print(f"  - First item keys: {list(item[0].keys())[:10]}")
                            else:
                                print(f"  - Type: {type(item)}")

                    # Look for total count
                    for key in ['total', 'totalCount', 'count', 'totalRecords']:
                        if key in data:
                            print(f"Total records available: {data[key]}")

                elif isinstance(data, list):
                    print(f"Response is a list with {len(data)} items")
                    if len(data) > 0:
                        print(f"First item keys: {list(data[0].keys())[:10]}")

                # Show preview
                print(f"\nResponse preview:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                print("...")

                success = True
                print(f"\n{'='*60}")
                print(f"✅ ENDPOINT WORKS!")
                print(f"{'='*60}")
                print(f"\nRun the scraper with:")
                print(f"  python3 scrape.py --api-endpoint {endpoint} --test")
                break

            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
        else:
            print(f"❌ HTTP {response.status_code}")

    except requests.exceptions.Timeout:
        print("⏱️  Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if not success:
    print(f"\n{'='*60}")
    print(f"❌ Endpoint doesn't seem to work with common parameters")
    print(f"{'='*60}")
    print("\nTry:")
    print(f"1. Verify the endpoint path is correct")
    print(f"2. Check the Network tab in browser for the exact parameters used")
    print(f"3. Try a different endpoint")
