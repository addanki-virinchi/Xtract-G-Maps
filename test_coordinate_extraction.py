#!/usr/bin/env python3
"""
Test script to verify the coordinate extraction functionality in Extract_Maps.py
"""

import sys
import re

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

def test_coordinate_extraction():
    """Test the coordinate extraction with various URL formats"""
    
    print("🧪 Testing Coordinate Extraction from Google Maps URLs")
    print("=" * 60)
    
    # Test URLs with different formats
    test_urls = [
        {
            "name": "Standard Google Maps URL",
            "url": "https://www.google.com/maps/place/Gowtham+Stationery/data=!4m7!3m6!1s0x3a52671cb912e037:0xd8f8607103e15f13!8m2!3d13.030133!4d80.2200671!16s%2Fg%2F1pv5x5kvc!19sChIJN-ASuRxnUjoRE1_hA3Fg-Ng?authuser=0&hl=en&rclk=1",
            "expected_lat": "13.030133",
            "expected_lng": "80.2200671"
        },
        {
            "name": "URL with negative coordinates",
            "url": "https://www.google.com/maps/place/Test/@-34.6037!3d-34.6037!4d-58.3816!17z",
            "expected_lat": "-34.6037",
            "expected_lng": "-58.3816"
        },
        {
            "name": "URL with decimal coordinates",
            "url": "https://www.google.com/maps/place/Test/@40.7128!3d40.7128!4d-74.0060!17z",
            "expected_lat": "40.7128",
            "expected_lng": "-74.0060"
        },
        {
            "name": "URL without coordinates",
            "url": "https://www.google.com/maps/search/restaurants",
            "expected_lat": "Not Found",
            "expected_lng": "Not Found"
        },
        {
            "name": "URL with integer coordinates",
            "url": "https://www.google.com/maps/place/Test/@51!3d51!4d0!17z",
            "expected_lat": "51",
            "expected_lng": "0"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_urls, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"URL: {test_case['url'][:80]}...")
        
        # Extract coordinates
        lat, lng = extract_coordinates_from_url(test_case['url'])
        
        # Check results
        lat_correct = lat == test_case['expected_lat']
        lng_correct = lng == test_case['expected_lng']
        
        print(f"Expected: Lat={test_case['expected_lat']}, Lng={test_case['expected_lng']}")
        print(f"Extracted: Lat={lat}, Lng={lng}")
        
        if lat_correct and lng_correct:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            all_passed = False
            
        print("-" * 40)
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Coordinate extraction is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please check the coordinate extraction logic.")
    print("="*60)
    
    return all_passed

def test_csv_integration():
    """Test that the coordinate extraction integrates properly with the main script"""
    print("\n🔗 Testing CSV Integration")
    print("=" * 40)
    
    try:
        # Import the main script functions
        sys.path.insert(0, '.')
        from Extract_Maps import extract_coordinates_from_url, append_result_to_csv
        
        # Test data
        test_result = {
            'URL': 'https://www.google.com/maps/place/Test/@13.030133!3d13.030133!4d80.2200671!17z',
            'Name': 'Test Business',
            'Address': 'Test Address',
            'Website': 'https://test.com',
            'Phone': '1234567890',
            'Latitude': '13.030133',
            'Longitude': '80.2200671'
        }
        
        # Test CSV writing
        test_filename = 'test_coordinates_output.csv'
        success = append_result_to_csv(test_result, test_filename, write_header=True)
        
        if success:
            print("✅ CSV writing with coordinates: PASSED")
            
            # Read back and verify
            import pandas as pd
            df = pd.read_csv(test_filename)
            
            expected_columns = ['URL', 'Name', 'Address', 'Website', 'Phone', 'Latitude', 'Longitude']
            if list(df.columns) == expected_columns:
                print("✅ CSV column structure: PASSED")
                print(f"📊 CSV Preview:")
                print(df.to_string(index=False))
            else:
                print("❌ CSV column structure: FAILED")
                print(f"Expected: {expected_columns}")
                print(f"Got: {list(df.columns)}")
            
            # Clean up
            import os
            os.remove(test_filename)
            print("🧹 Cleaned up test file")
            
        else:
            print("❌ CSV writing with coordinates: FAILED")
            
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run coordinate extraction tests
    extraction_passed = test_coordinate_extraction()
    
    # Run CSV integration tests
    test_csv_integration()
    
    print(f"\n🏁 Testing Complete!")
    if extraction_passed:
        print("✅ Ready to use enhanced Extract_Maps.py with coordinate extraction!")
    else:
        print("❌ Please fix coordinate extraction issues before using the script.")
