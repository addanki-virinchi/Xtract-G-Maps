# Real-Time Incremental Data Saving Guide

## Overview
The Google Maps scraper now implements **real-time incremental data saving** instead of batch processing. This means data is saved immediately after each individual search operation, providing better fault tolerance and lower memory usage.

## How It Works

### Previous Batch Approach (OLD)
```
For each search term:
  1. Collect results from ALL pin codes in memory
  2. Save all results to individual CSV at once
  3. Add all results to master collection
  4. Continue to next search term
  5. At the end, save master CSV with all data
```

### New Real-Time Approach (NEW)
```
For each search term:
  For each pin code:
    1. Perform search (search_term + pincode)
    2. IMMEDIATELY append results to individual CSV
    3. IMMEDIATELY append results to master CSV (with duplicate detection)
    4. Continue to next pin code
  Continue to next search term
```

## Key Benefits

### 🛡️ **Fault Tolerance**
- **Problem Solved**: If script crashes, no data is lost
- **How**: Data is written to disk immediately after each search
- **Result**: Can see partial results even if script is interrupted

### 💾 **Lower Memory Usage**
- **Problem Solved**: No large data collections stored in memory
- **How**: Results are written to CSV immediately, not accumulated
- **Result**: Script uses minimal memory regardless of how many results are found

### 👀 **Real-Time Progress Visibility**
- **Problem Solved**: Can see progress as it happens
- **How**: CSV files grow in real-time, console shows immediate save confirmations
- **Result**: Know immediately if searches are working and producing results

### 🔄 **Resume Capability**
- **Problem Solved**: Can continue from where it left off if interrupted
- **How**: Individual and master CSV files contain all completed searches
- **Result**: Manual resume possible by modifying search terms list

## File Writing Behavior

### Individual CSV Files
- **File Creation**: Created when first result for that search term is found
- **Writing**: Appends results after each pincode search
- **Header**: Written only once when file is first created
- **Duplicates**: No duplicate detection (same URL can appear multiple times if found in different pin codes)

### Master CSV File
- **File Creation**: Created when first result from any search is found
- **Writing**: Appends results after each pincode search
- **Header**: Written only once when file is first created
- **Duplicates**: Duplicate URLs are filtered out automatically

## Console Output Examples

### Successful Search with Results
```
[15/520] Processing: Stationery store in 600003
Pin code 3/20 for search term 'Stationery store'
Found 4 results. Saving immediately...
Appended 4 results to stationery_store_results.csv
Added 2 new unique entries to master CSV
✅ Saved: 4 to individual CSV, 2 new to master CSV
Waiting 10 seconds before next search...
```

### Search with No Results
```
[16/520] Processing: Stationery store in 600004
Pin code 4/20 for search term 'Stationery store'
No results found for Stationery store in 600004
Waiting 10 seconds before next search...
```

### Search with Error
```
[17/520] Processing: Stationery store in 600005
Pin code 5/20 for search term 'Stationery store'
❌ Error in search 'Stationery store 600005': Timeout waiting for element
Continuing to next search...
```

## File Structure During Execution

As the script runs, you'll see files being created and growing:

```
Google_Map/Maps_Ex/
├── stationery_store_results.csv          (Growing in real-time)
├── stationery_shop_results.csv           (Created when first result found)
├── school_supplies_store_results.csv     (Created when first result found)
├── stationery_shops_chennai_master.csv   (Growing with all results)
└── ... (other files created as searches progress)
```

## Monitoring Progress

### Real-Time File Monitoring
You can monitor progress by checking file sizes:
```bash
# Windows Command Prompt
dir *.csv

# PowerShell
Get-ChildItem *.csv | Select-Object Name, Length, LastWriteTime

# Check line count in real-time
findstr /R /N "^" stationery_shops_chennai_master.csv | find /C ":"
```

### CSV File Contents
Each CSV file contains these columns:
- `URL`: Google Maps URL for the business
- `Search_Term`: The search term used (e.g., "Stationery store")
- `Pincode`: The Chennai pincode searched (e.g., "600001")
- `Search_Query`: Combined search term + pincode (e.g., "Stationery store 600001")

## Error Recovery

### If Script Crashes
1. **Check existing CSV files** - All completed searches are already saved
2. **Count completed searches** - Check which search terms have CSV files
3. **Manual resume** - Modify the SEARCH_TERMS list to exclude completed terms
4. **Restart script** - Continue from where it left off

### If Duplicate Data Concerns
- **Individual CSVs**: May contain duplicates if same business found in multiple pin codes
- **Master CSV**: Automatically filters duplicates based on URL
- **Manual cleanup**: Use Excel or pandas to remove duplicates if needed

## Technical Implementation

### Key Functions
- `append_to_individual_csv()`: Writes to individual search term CSV files
- `append_to_master_csv()`: Writes to master CSV with duplicate detection
- `get_individual_csv_filename()`: Generates consistent filenames

### Duplicate Detection
- Uses URL as unique identifier
- Reads existing master CSV to check for duplicates before writing
- Only new URLs are added to master CSV
- Individual CSVs may contain duplicates (by design)

This real-time approach ensures maximum data preservation and provides immediate feedback on the scraping progress.
