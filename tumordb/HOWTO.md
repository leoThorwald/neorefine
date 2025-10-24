# How to Find the TumorAgDB API Endpoint

The scraper is ready to run, but we need to find the correct API endpoint first.

## Quick Start Guide

### Option 1: Manual Discovery (Recommended - 2 minutes)

1. **Open your browser** (Chrome, Firefox, or Safari)
2. **Navigate to**: https://tumoragdb.com.cn/#/search
3. **Open Developer Tools**:
   - Chrome/Firefox: Press `F12` or `Cmd+Option+I` (Mac)
   - Safari: Enable Developer menu first in Preferences, then `Cmd+Option+I`

4. **In Developer Tools**:
   - Click the **Network** tab
   - Check **"Preserve log"** (important!)
   - Filter by **"Fetch/XHR"** or **"All"**

5. **Trigger the API call**:
   - Perform a search on the website
   - Click pagination buttons
   - Or just load the search page

6. **Find the API endpoint**:
   - Look for requests in the Network tab
   - Look for requests that return JSON data
   - Click on the request to see details
   - Copy the path (e.g., `/api/neoantigen/search`)

7. **Run the scraper**:
   ```bash
   # Test first (only 3 pages)
   python3 scrape.py --api-endpoint /api/YOUR_ENDPOINT --test

   # If successful, run full scrape
   python3 scrape.py --api-endpoint /api/YOUR_ENDPOINT
   ```

### Option 2: Use Browser Network Export

If you're comfortable with it:

1. Follow steps 1-6 above
2. Right-click on the API request → "Copy as cURL"
3. Share the cURL command and I can extract the endpoint

### Option 3: Try Common Endpoints

The script can test these manually:

```bash
# Try these one by one
python3 scrape.py --api-endpoint /api/search --test
python3 scrape.py --api-endpoint /api/neoantigen/list --test
python3 scrape.py --api-endpoint /search --test
```

## What to Look For

Good API requests usually:
- Have "api" in the URL path
- Return JSON data (shown in the Response tab)
- Include pagination parameters like `page`, `size`, `pageNum`
- Show large amounts of neoantigen/tumor data

## Once You Find It

Share the endpoint with me (e.g., `/api/search`) and I'll help you run the full scrape!

## Script Features

- **--test**: Test mode (only 3 pages, ~300 records)
- **--pages N**: Number of pages to scrape (default: 1547)
- **--per-page N**: Records per page (default: 100)
- **--delay N**: Seconds between requests (default: 1.0)
- **--output FILE**: Output CSV filename
- **--checkpoint FILE**: Save/resume progress

## Example Commands

```bash
# Test with 3 pages
python3 scrape.py --api-endpoint /api/YOUR_ENDPOINT --test

# Full scrape with progress saving
python3 scrape.py --api-endpoint /api/YOUR_ENDPOINT --checkpoint progress.json

# Custom parameters
python3 scrape.py --api-endpoint /api/YOUR_ENDPOINT --pages 100 --per-page 50 --delay 0.5
```

## Need Help?

If you're stuck, you can:
1. Share a screenshot of the Network tab
2. Copy the cURL command of a working request
3. Share the endpoint path you found

The scraper is ready to go once we have the endpoint!
