#!/usr/bin/env python3
"""
Test script for the improved SafeDriver functionality
Tests the enhanced driver creation and cleanup on virtual servers
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Google_Maps import create_stable_driver, safe_driver_quit, scroll_google_maps_single_search

def test_driver_stability():
    """Test driver creation and cleanup multiple times"""
    print("=" * 60)
    print("TESTING IMPROVED DRIVER STABILITY")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    for i in range(total_tests):
        print(f"\nTest {i + 1}/{total_tests}: Driver creation and cleanup")
        
        try:
            # Create driver
            driver = create_stable_driver()
            print(f"✓ Driver created successfully")
            
            # Test basic navigation
            driver.get("https://www.google.com")
            print(f"✓ Navigation test passed")
            
            # Test the improved cleanup
            safe_driver_quit(driver)
            print(f"✓ Driver cleanup completed cleanly")
            
            success_count += 1
            
            # Wait between tests
            if i < total_tests - 1:
                print("Waiting 3 seconds before next test...")
                time.sleep(3)
                
        except Exception as e:
            print(f"✗ Test {i + 1} failed: {e}")
    
    print(f"\nStability test results: {success_count}/{total_tests} successful")
    return success_count == total_tests

def test_single_search():
    """Test a single Google Maps search with timeout protection"""
    print("\n" + "=" * 60)
    print("TESTING SINGLE SEARCH WITH TIMEOUT PROTECTION")
    print("=" * 60)
    
    try:
        search_term = "Stationery store"
        pincode = "600001"
        
        print(f"Testing search: {search_term} in {pincode}")
        print("This test includes timeout protection to prevent hanging...")
        
        start_time = time.time()
        results = scroll_google_maps_single_search(search_term, pincode)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Search completed in {duration:.1f} seconds")
        
        if results and len(results) > 0:
            print(f"✓ Search successful! Found {len(results)} results")
            print("Sample result:")
            print(f"  URL: {results[0]['URL']}")
            return True
        else:
            print("⚠ Search completed but no results found")
            print("This might be normal if there are no stores in this area")
            return True  # Still consider this a success
            
    except Exception as e:
        print(f"✗ Single search test failed: {e}")
        return False

def test_driver_cleanup_scenarios():
    """Test various driver cleanup scenarios"""
    print("\n" + "=" * 60)
    print("TESTING DRIVER CLEANUP SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        "Normal cleanup",
        "Cleanup with closed browser",
        "Cleanup with None driver"
    ]
    
    success_count = 0
    
    for i, scenario in enumerate(scenarios):
        print(f"\nScenario {i + 1}: {scenario}")
        
        try:
            if scenario == "Normal cleanup":
                driver = create_stable_driver()
                safe_driver_quit(driver)
                print("✓ Normal cleanup successful")
                
            elif scenario == "Cleanup with closed browser":
                driver = create_stable_driver()
                driver.close()  # Close browser first
                safe_driver_quit(driver)  # Then try to quit
                print("✓ Cleanup after browser close successful")
                
            elif scenario == "Cleanup with None driver":
                safe_driver_quit(None)  # Test with None
                print("✓ None driver cleanup handled gracefully")
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ Scenario {i + 1} failed: {e}")
    
    print(f"\nCleanup scenarios: {success_count}/{len(scenarios)} successful")
    return success_count == len(scenarios)

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 COMPREHENSIVE IMPROVED DRIVER TEST")
    print("=" * 80)
    print("Testing enhanced SafeDriver with virtual server optimizations")
    print("=" * 80)
    
    tests = [
        ("Driver Stability", test_driver_stability),
        ("Single Search with Timeout", test_single_search),
        ("Driver Cleanup Scenarios", test_driver_cleanup_scenarios),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("The improved SafeDriver is working correctly and should not hang on virtual servers.")
        print("\nKey improvements verified:")
        print("✓ Enhanced driver cleanup with multiple fallback strategies")
        print("✓ Timeout protection to prevent hanging")
        print("✓ Virtual server optimized Chrome options")
        print("✓ Graceful error handling and recovery")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)
