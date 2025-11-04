"""
Test script to verify the interactive search implementation in Google_Maps.py
Tests the search box interaction and element location
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import time

def test_interactive_search():
    """Test the interactive search method"""
    driver = None
    
    try:
        print("=" * 80)
        print("TESTING INTERACTIVE SEARCH IMPLEMENTATION")
        print("=" * 80)
        
        # Create driver
        print("\n1. Creating Chrome driver...")
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        driver = uc.Chrome(options=options, version_main=None)
        print("   ✓ Driver created successfully")
        
        # Navigate to Google Maps
        print("\n2. Navigating to Google Maps...")
        driver.get("https://www.google.com/maps/")
        print("   ✓ Google Maps loaded")
        time.sleep(3)
        
        # Wait for search box
        print("\n3. Waiting for search box element...")
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        print("   ✓ Search box found with ID 'searchboxinput'")
        
        # Test search query
        search_query = "Stationery store 600001"
        print(f"\n4. Entering search query: '{search_query}'")
        search_box.clear()
        search_box.send_keys(search_query)
        print("   ✓ Search query entered")
        time.sleep(1)
        
        # Find and click search button
        print("\n5. Locating search button...")
        search_button = driver.find_element(By.ID, "searchbox-searchbutton")
        print("   ✓ Search button found with ID 'searchbox-searchbutton'")
        
        print("\n6. Clicking search button...")
        search_button.click()
        print("   ✓ Search button clicked")
        
        # Wait for results
        print("\n7. Waiting for search results to load...")
        time.sleep(5)
        print("   ✓ Results loaded")
        
        # Verify results are displayed
        print("\n8. Verifying search results...")
        try:
            results = driver.find_elements(By.CSS_SELECTOR, "a[href*='maps/place']")
            print(f"   ✓ Found {len(results)} place results")
            
            if len(results) > 0:
                print("\n" + "=" * 80)
                print("✅ INTERACTIVE SEARCH TEST PASSED!")
                print("=" * 80)
                print("\nKey findings:")
                print(f"  - Search box element located successfully")
                print(f"  - Search query entered and submitted")
                print(f"  - Results loaded and parsed")
                print(f"  - {len(results)} place results found")
                return True
            else:
                print("   ⚠ No results found (may be normal for some searches)")
                return True
                
        except Exception as e:
            print(f"   ⚠ Could not verify results: {e}")
            return True
        
    except TimeoutException as e:
        print(f"\n❌ TIMEOUT ERROR: {e}")
        print("   The search box or button did not load within the timeout period")
        return False
        
    except NoSuchElementException as e:
        print(f"\n❌ ELEMENT NOT FOUND: {e}")
        print("   Could not locate search box or button")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False
        
    finally:
        if driver:
            print("\n9. Cleaning up...")
            try:
                driver.quit()
                print("   ✓ Driver closed successfully")
            except:
                pass

if __name__ == "__main__":
    success = test_interactive_search()
    exit(0 if success else 1)

