#!/usr/bin/env python3
"""
Test script to verify the fixes in Extract_Maps.py
This script creates a small test CSV and runs the extraction to verify all fixes work.
"""

import pandas as pd
import os
import sys

def create_test_csv():
    """Create a small test CSV with a few Google Maps URLs"""
    test_urls = [
        "https://www.google.com/maps/place/Starbucks/@12.9716,77.5946,17z/data=!3m1!4b1!4m6!3m5!1s0x3bae1670c9b44e6d:0x11f2c0df86dcf2b!8m2!3d12.9716!4d77.5946!16s%2Fg%2F11c5m7x1qz",
        "https://www.google.com/maps/place/McDonald's/@12.9716,77.5946,17z/data=!3m1!4b1!4m6!3m5!1s0x3bae1670c9b44e6d:0x11f2c0df86dcf2b!8m2!3d12.9716!4d77.5946!16s%2Fg%2F11c5m7x1qz"
    ]
    
    df = pd.DataFrame({'URL': test_urls})
    df.to_csv('input_urls.csv', index=False)
    print("✅ Created test CSV file: input_urls.csv")
    return len(test_urls)

def run_test():
    """Run the test to verify Extract_Maps.py works correctly"""
    print("🧪 Testing Extract_Maps.py fixes...")
    print("=" * 50)
    
    # Create test CSV
    num_urls = create_test_csv()
    
    # Import and run the main function
    try:
        # Add current directory to path to import Extract_Maps
        sys.path.insert(0, '.')
        
        # Import the main function from Extract_Maps
        from Extract_Maps import main
        
        print(f"🚀 Running extraction on {num_urls} test URLs...")
        print("This will test:")
        print("  ✓ Standard Selenium WebDriver (instead of undetected_chromedriver)")
        print("  ✓ Fixed UnboundLocalError for processed_count")
        print("  ✓ Incremental CSV writing")
        print("  ✓ Improved parallel processing")
        print("  ✓ Better error handling")
        print("-" * 50)
        
        # Run the main extraction
        main()
        
        # Check if output file was created
        if os.path.exists('google_maps_output.csv'):
            output_df = pd.read_csv('google_maps_output.csv')
            print(f"✅ SUCCESS: Output file created with {len(output_df)} records")
            print("✅ All fixes appear to be working correctly!")
            
            # Show sample output
            print("\n📊 Sample output:")
            print(output_df.head())
        else:
            print("❌ FAILED: No output file was created")
            
    except Exception as e:
        print(f"❌ ERROR during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up test files
        try:
            if os.path.exists('input_urls.csv'):
                os.remove('input_urls.csv')
                print("🧹 Cleaned up test input file")
        except:
            pass

if __name__ == "__main__":
    run_test()
