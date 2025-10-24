#!/usr/bin/env python3
"""Quick test of the peopleType endpoint with POST"""

import requests
import json

url = "https://tumoragdb.com.cn/proxy/api/peopleType"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
}

# Test with the exact parameters from the browser
payload = {"pageNum": 1, "pageSize": 100}

print(f"Testing: {url}")
print(f"Payload: {payload}")
print("-" * 60)

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(f"\nResponse type: {type(data)}")

        if isinstance(data, dict):
            print(f"Response keys: {list(data.keys())}")

            # Print full response to see structure
            print(f"\nFull response:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])

            # Look for data
            for key in ['data', 'records', 'rows', 'list', 'items']:
                if key in data:
                    items = data[key]
                    if isinstance(items, list):
                        print(f"\n'{key}' contains {len(items)} records")
                        if len(items) > 0:
                            print(f"First record keys: {list(items[0].keys())}")
                            print(f"\nFirst record sample:")
                            print(json.dumps(items[0], indent=2, ensure_ascii=False)[:500])
                    elif isinstance(items, dict):
                        print(f"\n'{key}' is a dict with keys: {list(items.keys())}")
                        print(json.dumps(items, indent=2, ensure_ascii=False)[:1000])
                    break

            # Look for total count
            for key in ['total', 'totalCount', 'count']:
                if key in data:
                    print(f"\nTotal records available: {data[key]}")

            # Also check nested data.total
            if 'data' in data and isinstance(data['data'], dict):
                if 'total' in data['data']:
                    print(f"\nTotal records (data.total): {data['data']['total']}")

        print("\n" + "=" * 60)
        print("✅ Endpoint is working! Ready to run the scraper.")
        print("=" * 60)
    else:
        print(f"❌ HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"❌ Error: {e}")
