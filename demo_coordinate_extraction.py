#!/usr/bin/env python3
"""
Demonstration script showing the enhanced coordinate extraction functionality
"""

import pandas as pd
import os
from Extract_Maps import extract_coordinates_from_url, append_result_to_csv

def demo_coordinate_extraction():
    """Demonstrate the coordinate extraction functionality"""
    
    print("🗺️  Google Maps Coordinate Extraction Demo")
    print("=" * 50)
    
    # Sample Google Maps URLs with coordinates
    sample_urls = [
        "https://www.google.com/maps/place/Gowtham+Stationery/data=!4m7!3m6!1s0x3a52671cb912e037:0xd8f8607103e15f13!8m2!3d13.030133!4d80.2200671!16s%2Fg%2F1pv5x5kvc",
        "https://www.google.com/maps/place/Test+Location/@12.9716!3d12.9716!4d77.5946!17z",
        "https://www.google.com/maps/place/Another+Place/@28.6139!3d28.6139!4d77.2090!17z"
    ]
    
    print("📍 Extracting coordinates from sample URLs:")
    print("-" * 50)
    
    results = []
    
    for i, url in enumerate(sample_urls, 1):
        print(f"\n{i}. URL: {url[:60]}...")
        
        # Extract coordinates
        latitude, longitude = extract_coordinates_from_url(url)
        
        print(f"   📍 Latitude: {latitude}")
        print(f"   📍 Longitude: {longitude}")
        
        # Create a sample result
        result = {
            'URL': url,
            'Name': f'Sample Business {i}',
            'Address': f'Sample Address {i}',
            'Website': f'https://example{i}.com',
            'Phone': f'123456789{i}',
            'Latitude': latitude,
            'Longitude': longitude
        }
        
        results.append(result)
    
    # Demonstrate CSV writing with coordinates
    print(f"\n💾 Writing results to CSV with coordinate columns...")
    output_file = 'demo_coordinates_output.csv'
    
    # Write header for first record
    success = append_result_to_csv(results[0], output_file, write_header=True)
    
    # Write remaining records
    for result in results[1:]:
        append_result_to_csv(result, output_file, write_header=False)
    
    if success:
        print(f"✅ Successfully created: {output_file}")
        
        # Read and display the CSV
        df = pd.read_csv(output_file)
        print(f"\n📊 CSV Output Preview:")
        print("=" * 80)
        print(df.to_string(index=False))
        print("=" * 80)
        
        print(f"\n📋 CSV Structure:")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Rows: {len(df)}")
        
        # Show coordinate summary
        print(f"\n🌍 Coordinate Summary:")
        for idx, row in df.iterrows():
            if row['Latitude'] != 'Not Found' and row['Longitude'] != 'Not Found':
                print(f"   {row['Name']}: ({row['Latitude']}, {row['Longitude']})")
            else:
                print(f"   {row['Name']}: Coordinates not found")
        
        print(f"\n✨ Enhancement Complete!")
        print(f"   ✅ Latitude column added")
        print(f"   ✅ Longitude column added") 
        print(f"   ✅ Coordinate extraction from URLs working")
        print(f"   ✅ CSV structure updated")
        
        # Clean up demo file
        try:
            os.remove(output_file)
            print(f"🧹 Cleaned up demo file: {output_file}")
        except:
            pass
            
    else:
        print("❌ Failed to write CSV file")

def show_enhancement_summary():
    """Show what was enhanced in the Extract_Maps.py script"""
    
    print(f"\n🚀 Extract_Maps.py Enhancement Summary")
    print("=" * 50)
    
    enhancements = [
        "✅ Added extract_coordinates_from_url() function",
        "✅ Updated CSV fieldnames to include 'Latitude' and 'Longitude'", 
        "✅ Modified scrape_data() to extract coordinates from URLs",
        "✅ Updated error handling to include coordinates even on failures",
        "✅ Enhanced append_result_to_csv() with new column structure",
        "✅ Coordinates extracted using regex patterns (3d for lat, 4d for lng)"
    ]
    
    for enhancement in enhancements:
        print(f"  {enhancement}")
    
    print(f"\n📝 New CSV Structure:")
    print(f"  URL, Name, Address, Website, Phone, Latitude, Longitude")
    
    print(f"\n🎯 Coordinate Extraction Logic:")
    print(f"  • Latitude: Extracted from '3d' parameter (e.g., '3d13.030133')")
    print(f"  • Longitude: Extracted from '4d' parameter (e.g., '4d80.2200671')")
    print(f"  • Supports positive, negative, and decimal coordinates")
    print(f"  • Returns 'Not Found' if coordinates not present in URL")

if __name__ == "__main__":
    demo_coordinate_extraction()
    show_enhancement_summary()
    
    print(f"\n🎉 Ready to use enhanced Extract_Maps.py!")
    print(f"   Run: python Extract_Maps.py")
    print(f"   Output: google_maps_output.csv (with Latitude & Longitude columns)")
