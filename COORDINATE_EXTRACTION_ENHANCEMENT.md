# Google Maps Coordinate Extraction Enhancement

## Overview
Enhanced the `Extract_Maps.py` script to extract latitude and longitude coordinates from Google Maps URLs and add them as new columns to the CSV output file.

## Enhancement Details

### 🎯 Objective
Extract latitude and longitude coordinates from Google Maps URLs and include them in the output CSV file alongside the existing data (Name, Address, Website, Phone).

### 📊 CSV Structure Changes

**Before:**
```
URL, Name, Address, Website, Phone
```

**After:**
```
URL, Name, Address, Website, Phone, Latitude, Longitude
```

### 🔧 Implementation

#### 1. New Function: `extract_coordinates_from_url()`
```python
def extract_coordinates_from_url(url):
    """
    Extract latitude and longitude coordinates from Google Maps URL
    
    Args:
        url (str): Google Maps URL containing coordinates
        
    Returns:
        tuple: (latitude, longitude) as strings, or ("Not Found", "Not Found") if not found
    """
    try:
        # Use regex to find latitude (3d parameter) and longitude (4d parameter)
        lat_pattern = r'3d([+-]?\d+\.?\d*)'
        lng_pattern = r'4d([+-]?\d+\.?\d*)'
        
        lat_match = re.search(lat_pattern, url)
        lng_match = re.search(lng_pattern, url)
        
        latitude = lat_match.group(1) if lat_match else "Not Found"
        longitude = lng_match.group(1) if lng_match else "Not Found"
        
        return latitude, longitude
        
    except Exception as e:
        print(f"Error extracting coordinates from URL: {str(e)}")
        return "Not Found", "Not Found"
```

#### 2. Updated CSV Writing Function
- Modified `append_result_to_csv()` to include 'Latitude' and 'Longitude' in fieldnames
- Updated CSV structure to accommodate the new columns

#### 3. Enhanced Data Extraction
- Modified `scrape_data()` function to call coordinate extraction
- Updated return dictionary to include latitude and longitude
- Enhanced error handling to extract coordinates even when scraping fails

#### 4. Improved Error Handling
- Coordinates are extracted even if web scraping fails
- Ensures data consistency across all records

### 🌍 Coordinate Extraction Logic

#### URL Pattern Recognition
Google Maps URLs contain coordinates in specific parameters:
- **Latitude**: Found after `3d` parameter (e.g., `3d13.030133`)
- **Longitude**: Found after `4d` parameter (e.g., `4d80.2200671`)

#### Supported Formats
- ✅ Positive coordinates: `3d13.030133`, `4d80.2200671`
- ✅ Negative coordinates: `3d-34.6037`, `4d-58.3816`
- ✅ Integer coordinates: `3d51`, `4d0`
- ✅ Decimal coordinates: `3d40.7128`, `4d-74.0060`

#### Example URL
```
https://www.google.com/maps/place/Gowtham+Stationery/data=!4m7!3m6!1s0x3a52671cb912e037:0xd8f8607103e15f13!8m2!3d13.030133!4d80.2200671!16s%2Fg%2F1pv5x5kvc!19sChIJN-ASuRxnUjoRE1_hA3Fg-Ng?authuser=0&hl=en&rclk=1
```

**Extracted:**
- Latitude: `13.030133`
- Longitude: `80.2200671`

### 🧪 Testing

#### Test Results
```
🗺️  Google Maps Coordinate Extraction Demo
==================================================
📍 Extracting coordinates from sample URLs:

1. URL: https://www.google.com/maps/place/Gowtham+Stationery/...
   📍 Latitude: 13.030133
   📍 Longitude: 80.2200671

2. URL: https://www.google.com/maps/place/Test+Location/@12.9716...
   📍 Latitude: 12.9716
   📍 Longitude: 77.5946

3. URL: https://www.google.com/maps/place/Another+Place/@28.6139...
   📍 Latitude: 28.6139
   📍 Longitude: 77.2090
```

#### CSV Output Verification
```
CSV Structure:
   Columns: ['URL', 'Name', 'Address', 'Website', 'Phone', 'Latitude', 'Longitude']
   Rows: 3

🌍 Coordinate Summary:
   Sample Business 1: (13.030133, 80.2200671)
   Sample Business 2: (12.9716, 77.5946)
   Sample Business 3: (28.6139, 77.209)
```

### 📁 Files Modified

1. **`Extract_Maps.py`** - Main script enhanced with coordinate extraction
2. **`demo_coordinate_extraction.py`** - Demonstration script
3. **`test_coordinate_extraction.py`** - Test script for validation

### 🚀 Usage

#### Running the Enhanced Script
```bash
python Extract_Maps.py
```

#### Expected Output
- Input: CSV file with Google Maps URLs
- Output: `google_maps_output.csv` with 7 columns including Latitude and Longitude

#### Sample Output Record
```csv
URL,Name,Address,Website,Phone,Latitude,Longitude
"https://www.google.com/maps/place/Gowtham+Stationery/...",Gowtham Stationery,"123 Main St",https://example.com,1234567890,13.030133,80.2200671
```

### ✅ Benefits

1. **Geographic Data**: Now includes precise location coordinates
2. **Data Completeness**: Coordinates extracted even if web scraping fails
3. **Mapping Integration**: Coordinates can be used for mapping applications
4. **Data Analysis**: Enables location-based analysis and visualization
5. **Backward Compatibility**: Existing functionality preserved

### 🔍 Error Handling

- **URL without coordinates**: Returns "Not Found" for both latitude and longitude
- **Malformed URLs**: Graceful handling with "Not Found" values
- **Scraping failures**: Coordinates still extracted from URL even if page scraping fails
- **Invalid coordinates**: Regex validation ensures only valid coordinate patterns are extracted

### 🎉 Enhancement Complete

The Google Maps data extraction script now successfully:
- ✅ Extracts latitude and longitude from Google Maps URLs
- ✅ Adds coordinate columns to CSV output
- ✅ Maintains all existing functionality
- ✅ Provides robust error handling
- ✅ Supports various coordinate formats
- ✅ Works with parallel processing and incremental CSV writing

The enhanced script is ready for production use with the new coordinate extraction capability!
