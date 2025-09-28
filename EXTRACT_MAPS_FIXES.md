# Extract_Maps.py - Issues Fixed + Real-Time Incremental Implementation

## Problems Resolved

### 1. ✅ **Regex Syntax Warnings Fixed**

**Problem**: SyntaxWarning messages about invalid escape sequences in regex patterns
```
SyntaxWarning: invalid escape sequence '\d'
```

**Locations Fixed**:
- Line 30: `re.findall(r'\d{3,}[-\s]?\d{3,}[-\s]?\d{3,}', phone_text)`
- Line 183: `re.findall(r'(?:\+?\d{1,4}[-.\s]?)?\d{3,}[-.\s]?\d{3,}[-.\s]?\d{3,}', phone_text)`
- Line 227: `re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{5}[-.\s]?\d{5}|\+\d{1,4}[-.\s]?\d+', phone_text)`
- Line 408: `re.findall(r'\d{3,}[-\s]?\d{3,}[-\s]?\d{4}', phone_text)`

**Solution**: All regex patterns now use raw strings (r'...') which properly handle escape sequences.

### 2. ✅ **Filename Spelling Corrected**

**Problem**: Script was looking for 'stationary_shops_chennai_master.csv' (incorrect spelling)
**Solution**: Changed to 'stationery_shops_chennai_master.csv' (correct spelling)

**Files Updated**:
- Input filename (line 305): `'stationery_shops_chennai_master.csv'`
- Output filename (line 344): `'stationery_shops_chennai_master_output.csv'`

### 3. ✅ **Enhanced Error Handling**

**Added Features**:
- File existence check before attempting to read CSV
- Column validation to ensure 'URL' column exists
- Better error messages with helpful suggestions
- Safe Chrome driver cleanup to prevent handle errors

### 4. ✅ **Chrome Driver Cleanup**

**Problem**: Potential Chrome driver handle errors similar to Google_Maps.py
**Solution**: Added `safe_driver_quit()` function with proper error handling

### 5. ✅ **Real-Time Incremental CSV Appending**

**Problem**: Script processed all URLs and saved results only at the end (batch processing)
**Solution**: Implemented real-time incremental saving after each URL extraction

**Benefits**:
- **Fault Tolerance**: Data saved even if script crashes mid-execution
- **Real-Time Progress**: See output file growing as URLs are processed
- **Lower Memory Usage**: No large result collections stored in memory
- **Resume Capability**: Automatically skip already processed URLs if interrupted

## New Features Added

### 📁 **File Validation**
```python
# Check if input file exists
if not os.path.exists(input_filename):
    print(f"Error: Input file '{input_filename}' not found!")
    print("Please run Google_Maps.py first to generate the master CSV file.")
    return
```

### 🔍 **Column Validation**
```python
# Verify URL column exists
if 'URL' not in df.columns:
    print(f"Error: 'URL' column not found")
    print(f"Available columns: {list(df.columns)}")
    return
```

### 🛡️ **Safe Driver Cleanup**
```python
def safe_driver_quit(driver):
    """Safely quit Chrome driver with error handling"""
    # Multiple fallback strategies for driver cleanup
```

### 🔄 **Real-Time CSV Appending**
```python
def append_result_to_csv(result, output_filename, write_header=False):
    """Append a single result to CSV immediately after extraction"""
    # Immediate writing to disk after each URL processing

def check_url_already_processed(url, output_filename):
    """Check if URL was already processed for resume capability"""
    # Enables automatic resume from where it left off
```

## Usage Instructions

### 1. **Prerequisites**
- Run `Google_Maps.py` first to generate the master CSV file
- Ensure the file `stationery_shops_chennai_master.csv` exists

### 2. **Test Before Running**
```bash
python test_extract_maps.py
```
This will verify:
- ✅ Input file exists and is readable
- ✅ Required 'URL' column is present
- ✅ Show sample data and file statistics

### 3. **Run the Extractor**
```bash
python Extract_Maps.py
```

### 4. **Expected Output**
- Input: `stationery_shops_chennai_master.csv`
- Output: `stationery_shops_chennai_master_output.csv`
- Columns: URL, Name, Address, Website, Phone

## Error Messages and Solutions

### ❌ "No such file or directory: 'stationery_shops_chennai_master.csv'"
**Solution**: Run `Google_Maps.py` first to generate the master CSV file

### ❌ "'URL' column not found"
**Solution**: Check that the input CSV file has the correct structure

### ❌ "SyntaxWarning: invalid escape sequence"
**Solution**: ✅ Already fixed - all regex patterns now use raw strings

### ❌ Chrome driver handle errors
**Solution**: ✅ Already fixed - using safe_driver_quit() function

## File Structure

After running both scripts, you should have:
```
Google_Map/Maps_Ex/
├── Google_Maps.py                              (Main scraper)
├── Extract_Maps.py                             (Data extractor - FIXED)
├── test_extract_maps.py                        (Test script)
├── stationery_shops_chennai_master.csv         (Input - from Google_Maps.py)
├── stationery_shops_chennai_master_output.csv  (Output - from Extract_Maps.py)
├── stationery_store_results.csv                (Individual results)
├── stationery_shop_results.csv                 (Individual results)
└── ... (other individual CSV files)
```

## Testing

### Quick Test
```bash
python test_extract_maps.py
```

### Full Workflow Test
```bash
# 1. Generate master CSV
python Google_Maps.py

# 2. Test file availability
python test_extract_maps.py

# 3. Extract detailed data
python Extract_Maps.py
```

## Summary of Changes

1. **Fixed all regex syntax warnings** by using raw strings
2. **Corrected filename spelling** from "stationary" to "stationery"
3. **Added comprehensive error handling** with helpful messages
4. **Implemented safe Chrome driver cleanup** to prevent handle errors
5. **Added file and column validation** before processing
6. **Created test script** to verify setup before running
7. **Enhanced output messages** with progress tracking

The Extract_Maps.py script is now robust, error-free, and properly integrated with the Google_Maps.py workflow.
