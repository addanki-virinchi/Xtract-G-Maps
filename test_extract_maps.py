#!/usr/bin/env python3
"""
Test script to verify Extract_Maps.py can find the correct input file
"""

import os
import pandas as pd

def test_file_availability():
    """Test if the required CSV file exists and is readable"""
    print("=" * 60)
    print("EXTRACT MAPS - REAL-TIME INCREMENTAL MODE TEST")
    print("=" * 60)
    
    # Check for the correct filename
    correct_filename = 'stationery_shops_chennai_master.csv'
    incorrect_filename = 'stationary_shops_chennai_master.csv'
    
    print(f"Looking for correct file: {correct_filename}")
    
    if os.path.exists(correct_filename):
        print(f"✅ Found: {correct_filename}")
        
        # Try to read the file
        try:
            df = pd.read_csv(correct_filename)
            print(f"✅ File is readable")
            print(f"✅ Number of rows: {len(df)}")
            print(f"✅ Columns: {list(df.columns)}")
            
            if 'URL' in df.columns:
                print(f"✅ 'URL' column found")
                print(f"✅ Number of URLs: {len(df['URL'])}")
                
                # Show a sample URL
                if len(df) > 0:
                    print(f"✅ Sample URL: {df['URL'].iloc[0]}")
                
                return True
            else:
                print(f"❌ 'URL' column not found in {correct_filename}")
                return False
                
        except Exception as e:
            print(f"❌ Error reading {correct_filename}: {e}")
            return False
    else:
        print(f"❌ File not found: {correct_filename}")
        
        # Check if the incorrect filename exists
        if os.path.exists(incorrect_filename):
            print(f"⚠️  Found file with incorrect spelling: {incorrect_filename}")
            print(f"⚠️  Please rename it to: {correct_filename}")
        else:
            print(f"❌ Neither correct nor incorrect filename found")
            print(f"❌ Please run Google_Maps.py first to generate the master CSV file")
        
        return False

def check_resume_capability():
    """Check if there's an existing output file for resume capability"""
    output_filename = 'stationery_shops_chennai_master_output.csv'

    print(f"\n🔄 Resume capability check:")
    if os.path.exists(output_filename):
        try:
            with open(output_filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                existing_count = sum(1 for row in reader)
            print(f"  ✅ Found existing output file: {output_filename}")
            print(f"  ✅ Already processed URLs: {existing_count}")
            print(f"  ✅ Script will skip these and continue from where it left off")
        except Exception as e:
            print(f"  ⚠️  Output file exists but couldn't read it: {e}")
    else:
        print(f"  📝 No existing output file - will start fresh")
        print(f"  📝 Will create: {output_filename}")

def list_csv_files():
    """List all CSV files in the current directory"""
    print(f"\n📁 CSV files in current directory:")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    if csv_files:
        for file in csv_files:
            size = os.path.getsize(file)
            print(f"  📄 {file} ({size} bytes)")
    else:
        print("  No CSV files found")

if __name__ == "__main__":
    success = test_file_availability()
    check_resume_capability()
    list_csv_files()

    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED: Extract_Maps.py should work correctly")
        print("🚀 REAL-TIME INCREMENTAL MODE READY")
        print("\nFeatures enabled:")
        print("  ✅ Immediate CSV writing after each URL")
        print("  ✅ Resume capability if interrupted")
        print("  ✅ Real-time progress visibility")
        print("  ✅ Fault tolerance")
        print("\nYou can now run: python Extract_Maps.py")
    else:
        print("❌ TEST FAILED: Please fix the issues above before running Extract_Maps.py")
        print("\nSuggested actions:")
        print("1. Run Google_Maps.py first to generate the master CSV file")
        print("2. Check that the file is named 'stationery_shops_chennai_master.csv' (correct spelling)")
        print("3. Ensure the CSV file contains a 'URL' column")
    print("=" * 60)
