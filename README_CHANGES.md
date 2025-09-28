# Google Maps Scraper - Updated Version

## Changes Made

### 1. **Fixed Chrome Driver Error**
- Added `safe_driver_quit()` function to handle Chrome driver cleanup properly
- Prevents the `OSError: [WinError 6] The handle is invalid` error
- Includes multiple fallback strategies for driver termination

### 2. **Real-Time Incremental Data Saving**
The script now implements immediate data saving for better fault tolerance:

**Previous Behavior:**
- Collected all results for a search term in memory
- Saved to CSV files only after processing all pin codes for that search term
- Risk of data loss if script crashed mid-execution

**New Behavior (Real-Time Incremental Saving):**
- After each individual search (search_term + pincode), immediately save results
- Append to individual CSV file for that search term
- Append to master CSV file (with duplicate detection)
- No batch collection in memory - everything saved immediately

### 3. **File Output Structure**

**Individual CSV Files (26 files):**
- `stationery_store_results.csv`
- `stationery_shop_results.csv`
- `school_supplies_store_results.csv`
- `office_supplies_store_results.csv`
- `bookstore_results.csv`
- ... (one for each search term)

**Master CSV File:**
- `stationery_shops_chennai_master.csv` - Contains ALL results from ALL search terms

### 4. **Benefits of Real-Time Saving**
- **Fault Tolerance**: Data is preserved even if script crashes
- **Lower Memory Usage**: No large data collections stored in memory
- **Real-Time Progress**: See results being written as they happen
- **Resume Capability**: Can continue from where it left off if interrupted
- **Immediate Feedback**: Know immediately if searches are successful

### 5. **Enhanced Error Handling**
- Better Chrome driver management
- Improved exception handling during scraping
- Graceful handling of failed searches

### 6. **Progress Tracking**
- Clear section headers for each search term
- Progress indicators showing current search term and pincode
- Real-time saving confirmation messages
- Summary statistics at completion

## How to Use

### Option 1: Run Full Script
```bash
python Google_Maps.py
```
This will:
- Process all 26 search terms
- For each search term, search across all 20 Chennai pin codes
- Create 26 individual CSV files + 1 master CSV file
- Total: ~520 searches (26 × 20)

### Option 2: Test First (Recommended)
```bash
python test_script.py
```
This will:
- Run a single test search to verify everything works
- Help identify any issues before running the full script

## Expected Output

### Console Output (Real-Time Saving)
```
PROCESSING SEARCH TERM 1/26: 'Stationery store'
================================================================================
[1/520] Processing: Stationery store in 600001
Pin code 1/20 for search term 'Stationery store'
Found 3 results. Saving immediately...
Appended 3 results to stationery_store_results.csv
Added 3 new unique entries to master CSV
✅ Saved: 3 to individual CSV, 3 new to master CSV
Waiting 10 seconds before next search...

[2/520] Processing: Stationery store in 600002
Pin code 2/20 for search term 'Stationery store'
Found 2 results. Saving immediately...
Appended 2 results to stationery_store_results.csv
Added 1 new unique entries to master CSV
✅ Saved: 2 to individual CSV, 1 new to master CSV
...
COMPLETED SEARCH TERM: 'Stationery store'
Total results found: 45
Individual CSV: stationery_store_results.csv
```

### File Output
```
Google_Map/Maps_Ex/
├── stationery_store_results.csv          (Results for "Stationery store" across all pin codes)
├── stationery_shop_results.csv           (Results for "Stationery shop" across all pin codes)
├── school_supplies_store_results.csv     (Results for "School supplies store" across all pin codes)
├── ...                                   (24 more individual CSV files)
└── stationery_shops_chennai_master.csv   (ALL results from ALL search terms)
```

## CSV File Structure
Each CSV file contains these columns:
- `URL`: Google Maps URL for the business
- `Search_Term`: The search term used
- `Pincode`: The Chennai pincode searched
- `Search_Query`: Combined search term + pincode

## Troubleshooting

### If Chrome Driver Issues Persist:
1. Update Chrome browser to latest version
2. Update undetected-chromedriver: `pip install --upgrade undetected-chromedriver`
3. Try running the test script first

### If Scraping is Blocked:
- The script includes 10-second delays between searches
- If still blocked, increase the delay in the main function
- Consider running smaller batches of search terms

### Memory Issues:
- The script processes one search term at a time to minimize memory usage
- Each individual CSV is saved immediately after processing
- Master CSV is only created at the end

## Performance Notes
- Total estimated time: 2-3 hours for all searches
- Each search takes ~20-30 seconds including delays
- **Real-time saving**: Results saved immediately after each search
- **Fault tolerant**: Can be interrupted and resumed (manually restart from where it left off)
- **Memory efficient**: No large data collections stored in memory
- **Progress visible**: CSV files grow in real-time as searches complete
