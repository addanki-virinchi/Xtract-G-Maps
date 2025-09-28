#!/usr/bin/env python3
"""
Test script to verify the Google Maps scraper functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Google_Maps import scroll_google_maps_single_search, append_to_individual_csv, append_to_master_csv, get_individual_csv_filename

def test_single_search():
    """Test a single search to verify the script works"""
    print("Testing single search functionality...")

    # Test with a simple search term and one pincode
    search_term = "Stationery store"
    pincode = "600001"

    try:
        results = scroll_google_maps_single_search(search_term, pincode)
        print(f"Search completed successfully!")
        print(f"Found {len(results)} results for '{search_term} {pincode}'")

        if results:
            print("Sample result:")
            print(f"  URL: {results[0]['URL']}")
            print(f"  Search Term: {results[0]['Search_Term']}")
            print(f"  Pincode: {results[0]['Pincode']}")

            # Test real-time saving functionality
            print("\nTesting real-time CSV saving...")

            # Test individual CSV saving
            individual_count = append_to_individual_csv(results, search_term)
            individual_filename = get_individual_csv_filename(search_term)
            print(f"✅ Saved {individual_count} results to {individual_filename}")

            # Test master CSV saving
            master_count = append_to_master_csv(results)
            print(f"✅ Saved {master_count} new results to master CSV")

            print("Real-time saving test completed successfully!")

        return True

    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GOOGLE MAPS SCRAPER TEST")
    print("=" * 60)
    
    success = test_single_search()
    
    if success:
        print("\n✅ Test passed! The script is working correctly.")
        print("You can now run the full script with confidence.")
    else:
        print("\n❌ Test failed! Please check the error messages above.")
    
    print("=" * 60)
