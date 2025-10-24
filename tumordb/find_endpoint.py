#!/usr/bin/env python3
"""
Enhanced API Endpoint Discovery Tool for TumorAgDB
This script attempts multiple strategies to find the correct API endpoint.
"""

import requests
import json
import re
from urllib.parse import urljoin

def test_endpoint(base_url, endpoint, params=None):
    """Test if an endpoint returns valid JSON data"""
    url = urljoin(base_url, endpoint)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': f'{base_url}/',
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                return True, data, response.status_code
            except:
                return False, None, response.status_code
        return False, None, response.status_code
    except Exception as e:
        return False, None, str(e)

def main():
    base_url = "https://tumoragdb.com.cn"

    print("=" * 70)
    print("🔍 TumorAgDB API Endpoint Discovery Tool")
    print("=" * 70)
    print()

    # Strategy 1: Try common API patterns
    print("📋 Strategy 1: Testing common API endpoint patterns...")
    print()

    endpoints = [
        # Search endpoints
        "/api/neoantigen/search",
        "/api/neoantigen/list",
        "/api/search",
        "/api/list",
        "/api/data",
        "/api/neoantigens",
        "/api/tumors",

        # Versioned endpoints
        "/api/v1/search",
        "/api/v1/neoantigen",
        "/api/v1/list",
        "/api/v2/search",

        # Alternative paths
        "/search/api",
        "/data/api",
        "/neoantigen/api",

        # Backend patterns
        "/backend/api/search",
        "/backend/search",
        "/service/search",

        # Common Chinese API patterns
        "/api/query",
        "/api/getList",
        "/api/getData",
    ]

    param_variations = [
        {"page": 1, "size": 10},
        {"page": 1, "pageSize": 10},
        {"pageNum": 1, "pageSize": 10},
        {"offset": 0, "limit": 10},
        {"current": 1, "pageSize": 10},
        {},
    ]

    found_endpoints = []

    for endpoint in endpoints:
        print(f"Testing: {endpoint}")
        for params in param_variations:
            success, data, status = test_endpoint(base_url, endpoint, params)

            if success and data:
                print(f"  ✅ SUCCESS with params: {params}")
                print(f"     Status: {status}")
                print(f"     Response type: {type(data)}")

                # Analyze response structure
                if isinstance(data, dict):
                    print(f"     Response keys: {list(data.keys())}")
                    if 'data' in data:
                        print(f"     'data' type: {type(data['data'])}")
                        if isinstance(data['data'], list) and len(data['data']) > 0:
                            print(f"     Sample record keys: {list(data['data'][0].keys())[:5]}")
                    if 'total' in data:
                        print(f"     Total records available: {data['total']}")
                elif isinstance(data, list) and len(data) > 0:
                    print(f"     Array length: {len(data)}")
                    print(f"     Sample record keys: {list(data[0].keys())[:5]}")

                print(f"     Preview: {str(data)[:200]}...")
                print()

                found_endpoints.append({
                    'endpoint': endpoint,
                    'params': params,
                    'data': data
                })
                break  # Found working params for this endpoint

    print()
    print("=" * 70)

    if found_endpoints:
        print(f"✅ Found {len(found_endpoints)} working endpoint(s)!")
        print()
        print("📝 To use with the scraper:")
        print()
        for i, ep in enumerate(found_endpoints, 1):
            print(f"{i}. python3 scrape.py --api-endpoint {ep['endpoint']} --test")
            print(f"   (with params: {ep['params']})")
            print()
    else:
        print("❌ No working endpoints found automatically.")
        print()
        print("🔍 Manual Discovery Steps:")
        print()
        print("1. Open Chrome/Firefox and go to: https://tumoragdb.com.cn/#/search")
        print("2. Press F12 to open Developer Tools")
        print("3. Go to the 'Network' tab")
        print("4. Check 'Preserve log' option")
        print("5. Filter by 'XHR' or 'Fetch' requests")
        print("6. Perform any search or navigation on the site")
        print("7. Look for requests that return JSON data")
        print("8. The endpoint path will be visible in the Network tab")
        print()
        print("Common patterns to look for:")
        print("  - Requests containing 'page', 'search', 'list', 'query' in URL")
        print("  - Responses with JSON data containing arrays of records")
        print("  - Look for 'Request URL' in the Headers tab of each request")
        print()

    # Strategy 2: Try to fetch and analyze the main page
    print("=" * 70)
    print("📋 Strategy 2: Analyzing main page for clues...")
    print()

    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            # Look for API endpoint hints in the HTML/JS
            content = response.text

            # Search for common API patterns in the page source
            api_patterns = [
                r'["\']/(api/[^"\']+)["\']',
                r'baseURL["\s:=]+["\']([^"\']+)["\']',
                r'axios\.(get|post)\(["\']([^"\']+)["\']',
                r'fetch\(["\']([^"\']+)["\']',
            ]

            potential_apis = set()
            for pattern in api_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        for m in match:
                            if '/' in m:
                                potential_apis.add(m)
                    else:
                        potential_apis.add(match)

            if potential_apis:
                print("🔍 Found potential API patterns in page source:")
                for api in sorted(potential_apis):
                    if 'api' in api.lower():
                        print(f"  - {api}")
                print()
                print("Try testing these manually with:")
                print(f"  python3 scrape.py --api-endpoint <endpoint> --test")
            else:
                print("⚠️  No obvious API patterns found in page source")

    except Exception as e:
        print(f"⚠️  Could not analyze main page: {e}")

    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
