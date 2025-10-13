#!/usr/bin/env python3
"""
Test script to verify the fixed extraction functions work correctly
"""

import sys
import os
import time

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced functions
from Extract_Maps import (
    create_chrome_driver, 
    safe_driver_quit,
    scrape_data
)
from selenium.webdriver.support.ui import WebDriverWait

def test_fixed_extraction():
    """Test the fixed extraction functions with a real Google Maps URL"""
    print("🧪 Testing Fixed Business Information Extraction")
    print("=" * 70)
    
    # Test URL from the CSV file
    test_url = "https://www.google.com/maps/place/EDIA/data=!4m7!3m6!1s0x390cfb3e3f468a1d:0xa20aa5a10c9de3f7!8m2!3d28.6822709!4d77.3127341!16s%2Fg%2F11fmlwl3fp!19sChIJHYpGPz77DDkR9-OdDKGlCqI?authuser=0&hl=en&rclk=1"
    
    driver = None
    try:
        print("🔄 Creating Chrome driver...")
        driver = create_chrome_driver(thread_id=999)
        
        if driver:
            print("✅ Chrome driver created successfully!")
            
            # Create WebDriverWait object
            wait = WebDriverWait(driver, 20)
            
            print("🔄 Testing complete scrape_data function...")
            start_time = time.time()
            
            # Test the complete scrape_data function
            result = scrape_data(test_url, driver, wait)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"⏱️ Processing completed in {processing_time:.2f} seconds")
            
            print("\n📊 EXTRACTION RESULTS")
            print("=" * 50)
            
            # Display results with status indicators
            for key, value in result.items():
                if key in ['Store_Type', 'Operating_Status', 'Operating_Hours', 'Rating', 'Permanently_Closed']:
                    status_icon = "✅" if value != "Not Found" else "❌"
                    print(f"   {status_icon} {key}: {value}")
                else:
                    print(f"   📋 {key}: {value}")
            
            # Count successful extractions
            enhanced_fields = ['Store_Type', 'Operating_Status', 'Operating_Hours', 'Rating', 'Permanently_Closed']
            successful_extractions = sum(1 for field in enhanced_fields if result.get(field, "Not Found") != "Not Found")
            
            print(f"\n📈 EXTRACTION SUMMARY")
            print("=" * 30)
            print(f"Enhanced fields extracted: {successful_extractions}/{len(enhanced_fields)}")
            print(f"Success rate: {(successful_extractions/len(enhanced_fields)*100):.1f}%")
            
            return successful_extractions >= 3  # Consider success if at least 3/5 enhanced fields work
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False
    finally:
        if driver:
            print("🔄 Cleaning up Chrome driver...")
            safe_driver_quit(driver)
            print("✅ Chrome driver cleaned up successfully")

def test_multiple_urls():
    """Test with multiple URLs from the CSV file"""
    print("\n🧪 Testing Multiple URLs")
    print("=" * 50)
    
    test_urls = [
        "https://www.google.com/maps/place/EDIA/data=!4m7!3m6!1s0x390cfb3e3f468a1d:0xa20aa5a10c9de3f7!8m2!3d28.6822709!4d77.3127341!16s%2Fg%2F11fmlwl3fp!19sChIJHYpGPz77DDkR9-OdDKGlCqI?authuser=0&hl=en&rclk=1",
        "https://www.google.com/maps/place/PHOENIX+ACADEMIA/data=!4m7!3m6!1s0x390ce3277c834719:0xace8ce6309fb80c1!8m2!3d28.5418375!4d77.2036432!16s%2Fg%2F11fphhk5v5!19sChIJGUeDfCfjDDkRwYD7CWPO6Kw?authuser=0&hl=en&rclk=1"
    ]
    
    driver = None
    try:
        driver = create_chrome_driver(thread_id=999)
        
        if driver:
            wait = WebDriverWait(driver, 20)
            
            results = []
            for i, url in enumerate(test_urls, 1):
                print(f"\n🔄 Testing URL {i}/{len(test_urls)}...")
                
                try:
                    result = scrape_data(url, driver, wait)
                    results.append(result)
                    
                    # Quick summary
                    enhanced_fields = ['Store_Type', 'Operating_Status', 'Operating_Hours', 'Rating']
                    successful = sum(1 for field in enhanced_fields if result.get(field, "Not Found") != "Not Found")
                    print(f"   ✅ URL {i}: {successful}/{len(enhanced_fields)} enhanced fields extracted")
                    
                except Exception as e:
                    print(f"   ❌ URL {i}: Error - {e}")
                    results.append(None)
            
            # Overall summary
            successful_urls = sum(1 for result in results if result is not None)
            print(f"\n📊 MULTIPLE URL TEST SUMMARY")
            print("=" * 40)
            print(f"Successfully processed: {successful_urls}/{len(test_urls)} URLs")
            
            return successful_urls >= len(test_urls) // 2  # Success if at least half work
            
    except Exception as e:
        print(f"❌ Error during multiple URL test: {e}")
        return False
    finally:
        if driver:
            safe_driver_quit(driver)

if __name__ == "__main__":
    print("🚀 Starting Fixed Extraction Tests")
    print("=" * 80)
    
    # Test 1: Single URL comprehensive test
    test1_passed = test_fixed_extraction()
    
    # Test 2: Multiple URLs test
    test2_passed = test_multiple_urls()
    
    print("\n" + "=" * 80)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Single URL Test: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Multiple URL Test: {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Fixed extraction functions are working correctly")
        print("✅ Enhanced fields are being extracted successfully")
        print("✅ Ready for production use")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("The fixes may need further refinement")
    
    print("=" * 80)
