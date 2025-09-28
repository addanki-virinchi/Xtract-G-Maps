# Extract_Maps.py - Real-Time Incremental Data Extraction

## Overview
The Extract_Maps.py script now implements **real-time incremental CSV appending** instead of batch processing. Data is saved immediately after extracting information from each URL, providing better fault tolerance and real-time progress visibility.

## How It Works

### Previous Batch Approach (OLD)
```
1. Process ALL URLs and collect results in memory
2. Save ALL results to CSV file at the end
3. If script crashes → lose all progress
```

### New Real-Time Approach (NEW)
```
For each URL:
  1. Extract data (Name, Address, Website, Phone)
  2. IMMEDIATELY append result to output CSV file
  3. Continue to next URL
  4. If script crashes → all processed URLs are already saved
```

## Key Benefits

### 🛡️ **Fault Tolerance**
- **Problem Solved**: Data preserved even if script crashes
- **How**: Each URL result written to CSV immediately after extraction
- **Result**: No data loss during interruptions

### 👀 **Real-Time Progress Visibility**
- **Problem Solved**: See progress as it happens
- **How**: Output CSV file grows in real-time
- **Result**: Monitor progress by checking file size/content

### 💾 **Lower Memory Usage**
- **Problem Solved**: No large data collections in memory
- **How**: Results written immediately, not accumulated
- **Result**: Minimal memory usage regardless of URL count

### 🔄 **Resume Capability**
- **Problem Solved**: Continue from where it left off if interrupted
- **How**: Checks existing output file and skips already processed URLs
- **Result**: Automatic resume without reprocessing

## New Functions Added

### `append_result_to_csv(result, output_filename, write_header=False)`
- Appends a single result to CSV immediately
- Handles header writing for new files
- Returns success/failure status

### `check_url_already_processed(url, output_filename)`
- Checks if URL was already processed (for resume capability)
- Reads existing output file to find processed URLs
- Returns True if URL already exists in output

## Console Output Examples

### Starting Fresh
```
================================================================================
STARTING REAL-TIME INCREMENTAL DATA EXTRACTION
================================================================================
Total URLs to process: 150
Output file: stationery_shops_chennai_master_output.csv
Mode: Real-time incremental CSV writing
--------------------------------------------------------------------------------

[1/150] Processing URL: https://maps.google.com/maps/place/...
✅ Extracted and saved: ABC Stationery Store
   Address: 123 Main Street, Chennai, Tamil Nadu 600001...
   Phone: +919876543210
   Progress: 1 new + 0 existing = 1/150
⏳ Waiting 2 seconds before next URL...
```

### Resuming from Previous Run
```
Found existing output file with 45 processed URLs
Will skip already processed URLs and continue from where left off

[46/150] Processing URL: https://maps.google.com/maps/place/...
⏭️  Skipping - already processed

[47/150] Processing URL: https://maps.google.com/maps/place/...
✅ Extracted and saved: XYZ Office Supplies
   Address: 456 Park Road, Chennai, Tamil Nadu 600002...
   Phone: +919123456789
   Progress: 1 new + 46 existing = 47/150
```

### Error Handling
```
[48/150] Processing URL: https://maps.google.com/maps/place/...
❌ Error processing URL: Timeout waiting for element
⏳ Waiting 2 seconds before next URL...
```

### Completion Summary
```
================================================================================
EXTRACTION COMPLETED!
================================================================================
Total URLs: 150
New URLs processed: 105
Already existing (skipped): 45
Errors encountered: 3
Output file: stationery_shops_chennai_master_output.csv
Total records in output file: 150
================================================================================
```

## File Structure During Execution

### Input File
- `stationery_shops_chennai_master.csv` (from Google_Maps.py)

### Output File (Growing in Real-Time)
- `stationery_shops_chennai_master_output.csv`
- **Columns**: URL, Name, Address, Website, Phone
- **Growth**: Adds one row after each URL processing

### Monitoring Progress
You can monitor real-time progress:

```bash
# Windows Command Prompt - Check file size
dir stationery_shops_chennai_master_output.csv

# PowerShell - Monitor file growth
Get-ChildItem stationery_shops_chennai_master_output.csv | Select-Object Name, Length, LastWriteTime

# Count lines in real-time (shows progress)
findstr /R /N "^" stationery_shops_chennai_master_output.csv | find /C ":"
```

## Resume Capability

### How Resume Works
1. **Check existing output file** - Script reads existing CSV on startup
2. **Count processed URLs** - Determines how many URLs already completed
3. **Skip processed URLs** - Automatically skips URLs already in output file
4. **Continue from next** - Processes only remaining URLs

### Manual Resume
If you need to manually resume:
1. **Check output file** - See which URLs were processed
2. **Modify input file** - Remove processed URLs from input CSV (optional)
3. **Restart script** - Will automatically skip existing URLs

## Error Recovery

### If Script Crashes
1. **Check output file** - All completed extractions are saved
2. **Restart script** - Will automatically resume from where it left off
3. **No data loss** - Previously extracted data is preserved

### If Extraction Errors Occur
- **Error records saved** - URLs with errors still get recorded with "Error" values
- **Script continues** - Errors don't stop processing of remaining URLs
- **Error tracking** - Final summary shows error count

## Performance Notes

### Timing
- **Per URL**: ~5-10 seconds (including 2-second delay)
- **Total time**: Depends on URL count (150 URLs ≈ 15-25 minutes)
- **Resume time**: Only processes remaining URLs

### Memory Usage
- **Minimal**: No large data collections in memory
- **Constant**: Memory usage doesn't grow with URL count
- **Efficient**: Only current URL data in memory at any time

### File I/O
- **Immediate writing**: Each result written to disk immediately
- **Append mode**: Efficient file operations
- **Header management**: Written only once per file

## Testing

### Pre-Run Test
```bash
python test_extract_maps.py
```
This checks:
- ✅ Input file exists and is readable
- ✅ Resume capability status
- ✅ File structure validation

### Monitor During Run
```bash
# In another terminal/command prompt
# Watch file grow in real-time
powershell -Command "while($true) { Get-ChildItem stationery_shops_chennai_master_output.csv | Select-Object Length, LastWriteTime; Start-Sleep 5 }"
```

## Troubleshooting

### "File not found" Error
- **Solution**: Run Google_Maps.py first to generate input file

### "Already processed" Messages
- **Normal**: Script is resuming from previous run
- **Action**: Let it continue - it will process remaining URLs

### High Error Count
- **Check**: Internet connection and Chrome driver
- **Action**: Restart script - it will retry failed URLs

This real-time approach ensures maximum data preservation and provides immediate feedback on extraction progress.
