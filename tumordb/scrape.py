#!/usr/bin/env python3
"""
TumorAgDB Data Scraper
Downloads data from tumoragdb.com.cn and exports to CSV

Usage:
    python tumoragdb_scraper.py [--pages PAGES] [--per-page SIZE] [--output FILE]

Requirements:
    pip install requests pandas tqdm
"""

import requests
import json
import csv
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not installed. Will use basic CSV writing.")

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Warning: tqdm not installed. Progress bar will not be shown.")


class TumorAgDBScraper:
    """Scraper for TumorAgDB database"""
    
    def __init__(self, base_url: str = "https://tumoragdb.com.cn"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': f'{base_url}/',
            'Content-Type': 'application/json',
        })
        self.api_endpoint = None
        self.all_data = []
        self.use_post = False
        
    def detect_api_endpoint(self) -> Optional[str]:
        """Try to detect the API endpoint by testing common patterns"""
        print("🔍 Detecting API endpoint...")
        
        # Common API endpoint patterns
        endpoints_to_try = [
            "/api/neoantigen/search",
            "/api/search",
            "/api/data/search",
            "/api/neoantigens",
            "/api/list",
            "/api/v1/search",
            "/api/v1/neoantigen",
            "/search/api",
            "/data/api/search",
        ]
        
        for endpoint in endpoints_to_try:
            url = f"{self.base_url}{endpoint}"
            try:
                # Try with pagination parameters
                for params in [
                    {"page": 1, "size": 10},
                    {"pageNum": 1, "pageSize": 10},
                    {"offset": 0, "limit": 10},
                    {}  # No params
                ]:
                    response = self.session.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if data and (isinstance(data, list) or 'data' in data or 'records' in data or 'items' in data):
                                print(f"✅ Found API endpoint: {endpoint}")
                                print(f"   Parameters: {params}")
                                print(f"   Response preview: {str(data)[:200]}...")
                                self.api_endpoint = endpoint
                                return endpoint
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                continue
        
        print("❌ Could not automatically detect API endpoint")
        print("You may need to inspect the network traffic in your browser to find the correct endpoint.")
        return None
    
    def fetch_page(self, page: int, page_size: int = 100, params: Dict = None) -> Optional[Dict]:
        """Fetch a single page of data"""
        if not self.api_endpoint:
            raise ValueError("API endpoint not set. Run detect_api_endpoint() first.")

        url = f"{self.base_url}{self.api_endpoint}"

        # Try different pagination parameter formats
        pagination_formats = [
            {"page": page, "size": page_size},
            {"pageNum": page, "pageSize": page_size},
            {"page": page, "per_page": page_size},
            {"offset": (page - 1) * page_size, "limit": page_size},
        ]

        if params:
            pagination_formats = [params]

        for page_params in pagination_formats:
            try:
                if self.use_post:
                    # POST request with JSON body
                    response = self.session.post(url, json=page_params, timeout=30)
                else:
                    # GET request with query parameters
                    response = self.session.get(url, params=page_params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    return {
                        'success': True,
                        'data': data,
                        'params': page_params,
                        'status_code': response.status_code
                    }
                elif response.status_code == 404:
                    continue
                else:
                    print(f"⚠️  Status {response.status_code} for page {page} with params {page_params}")

            except requests.exceptions.Timeout:
                print(f"⏱️  Timeout for page {page}, retrying...")
                time.sleep(2)
            except Exception as e:
                continue

        return None
    
    def extract_records(self, response_data: Any) -> List[Dict]:
        """Extract records from API response (handles various response structures)"""
        if isinstance(response_data, list):
            return response_data

        # Common response structure patterns
        possible_keys = ['data', 'records', 'items', 'results', 'list', 'content']

        for key in possible_keys:
            if isinstance(response_data, dict) and key in response_data:
                data = response_data[key]
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # Handle nested data structures (e.g., data.data)
                    if 'data' in data and isinstance(data['data'], list):
                        return data['data']
                    elif 'records' in data:
                        return data['records']
                    elif 'list' in data:
                        return data['list']

        # If response is a dict, wrap it in a list
        if isinstance(response_data, dict):
            return [response_data]

        return []
    
    def scrape_all_pages(self, total_pages: int = 1547, page_size: int = 100, 
                         start_page: int = 1, delay: float = 1.0) -> List[Dict]:
        """Scrape all pages of data"""
        print(f"\n📥 Starting scrape: {total_pages} pages, {page_size} records per page")
        print(f"   Total records expected: ~{total_pages * page_size:,}")
        print(f"   Delay between requests: {delay}s")
        
        self.all_data = []
        successful_pages = 0
        failed_pages = []
        
        # Create progress bar if tqdm is available
        page_range = range(start_page, total_pages + 1)
        if HAS_TQDM:
            page_range = tqdm(page_range, desc="Scraping pages", unit="page")
        
        for page in page_range:
            response = self.fetch_page(page, page_size)
            
            if response and response['success']:
                records = self.extract_records(response['data'])
                
                if records:
                    self.all_data.extend(records)
                    successful_pages += 1
                    
                    if not HAS_TQDM and page % 10 == 0:
                        print(f"   Progress: {page}/{total_pages} pages ({len(self.all_data):,} records)")
                else:
                    # No records might mean we've reached the end
                    if page > start_page:
                        print(f"\n⚠️  No records found on page {page}. May have reached the end.")
                        break
            else:
                failed_pages.append(page)
                if len(failed_pages) > 10:  # Stop if too many failures
                    print(f"\n❌ Too many failed pages. Stopping.")
                    break
            
            # Rate limiting
            time.sleep(delay)
        
        print(f"\n✅ Scraping complete!")
        print(f"   Successful pages: {successful_pages}/{total_pages}")
        print(f"   Total records: {len(self.all_data):,}")
        if failed_pages:
            print(f"   Failed pages: {len(failed_pages)} - {failed_pages[:10]}...")
        
        return self.all_data
    
    def save_to_csv(self, output_file: str = "tumoragdb_data.csv"):
        """Save scraped data to CSV file"""
        if not self.all_data:
            print("❌ No data to save")
            return
        
        print(f"\n💾 Saving {len(self.all_data):,} records to {output_file}...")
        
        if HAS_PANDAS:
            # Use pandas for better CSV handling
            df = pd.DataFrame(self.all_data)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
        else:
            # Fall back to basic CSV writer
            if self.all_data:
                keys = self.all_data[0].keys()
                with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(self.all_data)
        
        # Get file size
        file_size = Path(output_file).stat().st_size / (1024 * 1024)  # MB
        print(f"✅ Saved successfully!")
        print(f"   File: {output_file}")
        print(f"   Size: {file_size:.2f} MB")
        print(f"   Records: {len(self.all_data):,}")
    
    def save_checkpoint(self, checkpoint_file: str = "checkpoint.json"):
        """Save progress checkpoint"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'records_count': len(self.all_data),
            'data': self.all_data
        }
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        print(f"💾 Checkpoint saved: {checkpoint_file}")
    
    def load_checkpoint(self, checkpoint_file: str = "checkpoint.json") -> int:
        """Load progress from checkpoint"""
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
                self.all_data = checkpoint['data']
                print(f"✅ Loaded checkpoint: {len(self.all_data):,} records")
                return len(self.all_data)
        except FileNotFoundError:
            print("ℹ️  No checkpoint file found")
            return 0


def main():
    parser = argparse.ArgumentParser(description='Scrape TumorAgDB database')
    parser.add_argument('--pages', type=int, default=1547, help='Total number of pages (default: 1547)')
    parser.add_argument('--per-page', type=int, default=100, help='Records per page (default: 100)')
    parser.add_argument('--output', type=str, default='tumoragdb_data.csv', help='Output CSV file')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--start-page', type=int, default=1, help='Starting page number (default: 1)')
    parser.add_argument('--checkpoint', type=str, help='Checkpoint file to resume from')
    parser.add_argument('--api-endpoint', type=str, help='API endpoint (e.g., /api/search)')
    parser.add_argument('--test', action='store_true', help='Test mode: only fetch first 3 pages')
    parser.add_argument('--use-post', action='store_true', help='Use POST instead of GET requests')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🧬 TumorAgDB Data Scraper")
    print("=" * 70)
    
    scraper = TumorAgDBScraper()
    
    # Load checkpoint if specified
    start_page = args.start_page
    if args.checkpoint and Path(args.checkpoint).exists():
        records_loaded = scraper.load_checkpoint(args.checkpoint)
        if records_loaded > 0:
            # Calculate which page to resume from
            start_page = (records_loaded // args.per_page) + 1
            print(f"📍 Resuming from page {start_page}")
    
    # Detect or set API endpoint
    if args.api_endpoint:
        scraper.api_endpoint = args.api_endpoint
        scraper.use_post = args.use_post
        print(f"✅ Using provided API endpoint: {args.api_endpoint}")
        if args.use_post:
            print(f"✅ Using POST requests")
    else:
        scraper.detect_api_endpoint()
    
    if not scraper.api_endpoint:
        print("\n❌ Could not detect API endpoint. Please provide it manually with --api-endpoint")
        print("\nTo find the API endpoint:")
        print("1. Open https://tumoragdb.com.cn/#/search in your browser")
        print("2. Open Developer Tools (F12)")
        print("3. Go to Network tab")
        print("4. Perform a search on the website")
        print("5. Look for XHR/Fetch requests to find the API endpoint")
        print("6. Run this script again with --api-endpoint /your/api/endpoint")
        return
    
    # Test mode: only 3 pages
    if args.test:
        print("\n🧪 TEST MODE: Only fetching first 3 pages")
        args.pages = 3
    
    try:
        # Scrape data
        scraper.scrape_all_pages(
            total_pages=args.pages,
            page_size=args.per_page,
            start_page=start_page,
            delay=args.delay
        )
        
        # Save to CSV
        scraper.save_to_csv(args.output)
        
        # Save final checkpoint
        if args.checkpoint:
            scraper.save_checkpoint(args.checkpoint)
        
        print("\n" + "=" * 70)
        print("✅ SCRAPING COMPLETE!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        # Save checkpoint on interrupt
        if args.checkpoint:
            print("💾 Saving progress...")
            scraper.save_checkpoint(args.checkpoint)
        # Save whatever data we have
        if scraper.all_data:
            scraper.save_to_csv(args.output)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        # Try to save data on error
        if scraper.all_data and args.checkpoint:
            scraper.save_checkpoint(args.checkpoint)


if __name__ == "__main__":
    main()