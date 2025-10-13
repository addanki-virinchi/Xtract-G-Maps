#!/usr/bin/env python3
"""
Script to analyze current Google Maps page structure and identify correct selectors
"""

import sys
import os
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Chrome driver creation function
from Extract_Maps import create_chrome_driver, safe_driver_quit

def analyze_page_structure(url):
    """Analyze the Google Maps page structure to identify correct selectors"""
    print(f"🔍 Analyzing Google Maps page structure for:")
    print(f"URL: {url}")
    print("=" * 80)
    
    driver = None
    try:
        print("🔄 Creating Chrome driver...")
        driver = create_chrome_driver(thread_id=999)
        
        if driver:
            print("✅ Chrome driver created successfully!")
            
            print("🔄 Navigating to URL...")
            driver.get(url)
            time.sleep(8)  # Wait for page to fully load
            
            # Scroll to ensure all elements are loaded
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            print("\n📊 ANALYZING PAGE ELEMENTS")
            print("=" * 50)
            
            # 1. Analyze Store Type/Category elements
            print("\n🏪 1. STORE TYPE/CATEGORY ANALYSIS")
            print("-" * 40)
            analyze_store_type_elements(driver)
            
            # 2. Analyze Operating Status and Hours elements
            print("\n🕒 2. OPERATING STATUS & HOURS ANALYSIS")
            print("-" * 40)
            analyze_operating_hours_elements(driver)
            
            # 3. Analyze Rating elements
            print("\n⭐ 3. RATING ANALYSIS")
            print("-" * 40)
            analyze_rating_elements(driver)
            
            # 4. Analyze basic info elements
            print("\n📋 4. BASIC INFO ANALYSIS")
            print("-" * 40)
            analyze_basic_info_elements(driver)
            
            # 5. Page source analysis
            print("\n🔍 5. PAGE SOURCE KEYWORDS ANALYSIS")
            print("-" * 40)
            analyze_page_source_keywords(driver)
            
            return True
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False
    finally:
        if driver:
            print("\n🔄 Cleaning up Chrome driver...")
            safe_driver_quit(driver)
            print("✅ Chrome driver cleaned up successfully")

def analyze_store_type_elements(driver):
    """Analyze store type/category elements"""
    try:
        # Look for button elements that might contain category
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} button elements")
        
        category_candidates = []
        for i, button in enumerate(buttons[:20]):  # Check first 20 buttons
            try:
                text = button.text.strip()
                classes = button.get_attribute("class")
                jsaction = button.get_attribute("jsaction")
                
                if text and len(text) > 0 and len(text) < 50:
                    if any(keyword in text.lower() for keyword in ['store', 'shop', 'institute', 'academy', 'center', 'service']):
                        category_candidates.append({
                            'text': text,
                            'classes': classes,
                            'jsaction': jsaction
                        })
                        print(f"  ✅ Category candidate: '{text}'")
                        print(f"     Classes: {classes}")
                        print(f"     JSAction: {jsaction}")
                        
            except Exception:
                continue
        
        if not category_candidates:
            print("  ❌ No obvious category candidates found in buttons")
            
        # Look for span elements that might contain category
        spans = driver.find_elements(By.TAG_NAME, "span")
        print(f"\nFound {len(spans)} span elements")
        
        for i, span in enumerate(spans[:30]):  # Check first 30 spans
            try:
                text = span.text.strip()
                classes = span.get_attribute("class")
                
                if text and len(text) > 0 and len(text) < 50:
                    if any(keyword in text.lower() for keyword in ['store', 'shop', 'institute', 'academy', 'center', 'service']):
                        print(f"  ✅ Span category candidate: '{text}'")
                        print(f"     Classes: {classes}")
                        
            except Exception:
                continue
                
    except Exception as e:
        print(f"  ❌ Error analyzing store type: {e}")

def analyze_operating_hours_elements(driver):
    """Analyze operating hours and status elements"""
    try:
        # Look for elements containing "Open", "Closed", "Hours"
        all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Open') or contains(text(), 'Closed') or contains(text(), 'Hours') or contains(text(), 'pm') or contains(text(), 'am')]")
        
        print(f"Found {len(all_elements)} elements with time/status keywords")
        
        for element in all_elements[:10]:  # Check first 10
            try:
                text = element.text.strip()
                tag_name = element.tag_name
                classes = element.get_attribute("class")
                
                if text and len(text) > 0:
                    print(f"  ✅ Hours candidate: '{text}'")
                    print(f"     Tag: {tag_name}, Classes: {classes}")
                    
            except Exception:
                continue
                
        # Look specifically for table elements (hours table)
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"\nFound {len(tables)} table elements")
        
        for table in tables:
            try:
                text = table.text.strip()
                classes = table.get_attribute("class")
                
                if "am" in text or "pm" in text or ":" in text:
                    print(f"  ✅ Hours table candidate:")
                    print(f"     Classes: {classes}")
                    print(f"     Text preview: {text[:100]}...")
                    
            except Exception:
                continue
                
    except Exception as e:
        print(f"  ❌ Error analyzing operating hours: {e}")

def analyze_rating_elements(driver):
    """Analyze rating elements"""
    try:
        # Look for elements that might contain ratings
        rating_patterns = [r'\d\.\d', r'^[1-5]$', r'^[1-5]\.[0-9]$']
        
        all_spans = driver.find_elements(By.TAG_NAME, "span")
        print(f"Found {len(all_spans)} span elements")
        
        rating_candidates = []
        for span in all_spans:
            try:
                text = span.text.strip()
                classes = span.get_attribute("class")
                aria_hidden = span.get_attribute("aria-hidden")
                
                if text:
                    for pattern in rating_patterns:
                        if re.match(pattern, text):
                            try:
                                rating_val = float(text)
                                if 0 <= rating_val <= 5:
                                    rating_candidates.append({
                                        'text': text,
                                        'classes': classes,
                                        'aria_hidden': aria_hidden
                                    })
                                    print(f"  ✅ Rating candidate: '{text}'")
                                    print(f"     Classes: {classes}")
                                    print(f"     Aria-hidden: {aria_hidden}")
                                    break
                            except ValueError:
                                continue
                                
            except Exception:
                continue
        
        if not rating_candidates:
            print("  ❌ No obvious rating candidates found")
            
        # Look for star elements
        star_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'star') or contains(@aria-label, 'star')]")
        print(f"\nFound {len(star_elements)} star-related elements")
        
    except Exception as e:
        print(f"  ❌ Error analyzing rating: {e}")

def analyze_basic_info_elements(driver):
    """Analyze basic info elements (name, address, website, phone)"""
    try:
        # Analyze name elements
        print("📝 NAME ANALYSIS:")
        h1_elements = driver.find_elements(By.TAG_NAME, "h1")
        for h1 in h1_elements:
            try:
                text = h1.text.strip()
                classes = h1.get_attribute("class")
                if text:
                    print(f"  ✅ H1 candidate: '{text}'")
                    print(f"     Classes: {classes}")
            except Exception:
                continue
        
        # Analyze address elements
        print("\n📍 ADDRESS ANALYSIS:")
        address_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'Io6YTe') or contains(@class, 'rogA2c')]")
        for addr in address_elements[:5]:
            try:
                text = addr.text.strip()
                classes = addr.get_attribute("class")
                if text and len(text) > 10:
                    print(f"  ✅ Address candidate: '{text[:50]}...'")
                    print(f"     Classes: {classes}")
            except Exception:
                continue
        
        # Analyze website elements
        print("\n🌐 WEBSITE ANALYSIS:")
        website_links = driver.find_elements(By.XPATH, "//a[contains(@aria-label, 'Website') or contains(@href, 'http')]")
        for link in website_links[:5]:
            try:
                href = link.get_attribute("href")
                aria_label = link.get_attribute("aria-label")
                if href and "google.com" not in href:
                    print(f"  ✅ Website candidate: {href}")
                    print(f"     Aria-label: {aria_label}")
            except Exception:
                continue
                
    except Exception as e:
        print(f"  ❌ Error analyzing basic info: {e}")

def analyze_page_source_keywords(driver):
    """Analyze page source for relevant keywords and class names"""
    try:
        page_source = driver.page_source
        
        # Look for common Google Maps class patterns
        class_patterns = [
            r'class="[^"]*DkEaL[^"]*"',
            r'class="[^"]*ZDu9vd[^"]*"',
            r'class="[^"]*F7nice[^"]*"',
            r'class="[^"]*Io6YTe[^"]*"',
            r'class="[^"]*rogA2c[^"]*"',
            r'class="[^"]*DUwDvf[^"]*"'
        ]
        
        print("🔍 CLASS NAME ANALYSIS:")
        for pattern in class_patterns:
            matches = re.findall(pattern, page_source)
            if matches:
                print(f"  ✅ Found {len(matches)} matches for pattern: {pattern}")
                if matches:
                    print(f"     Example: {matches[0]}")
            else:
                print(f"  ❌ No matches for pattern: {pattern}")
        
        # Look for specific keywords
        keywords = ['Open', 'Closed', 'Hours', 'Rating', 'Store', 'Institute', 'Academy']
        print(f"\n🔍 KEYWORD ANALYSIS:")
        for keyword in keywords:
            count = page_source.lower().count(keyword.lower())
            print(f"  '{keyword}': {count} occurrences")
            
    except Exception as e:
        print(f"  ❌ Error analyzing page source: {e}")

if __name__ == "__main__":
    # Test with a URL from the CSV file
    test_url = "https://www.google.com/maps/place/EDIA/data=!4m7!3m6!1s0x390cfb3e3f468a1d:0xa20aa5a10c9de3f7!8m2!3d28.6822709!4d77.3127341!16s%2Fg%2F11fmlwl3fp!19sChIJHYpGPz77DDkR9-OdDKGlCqI?authuser=0&hl=en&rclk=1"
    
    print("🚀 Starting Google Maps Page Structure Analysis")
    print("=" * 80)
    
    success = analyze_page_structure(test_url)
    
    print("\n" + "=" * 80)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 80)
    
    if success:
        print("🎉 ANALYSIS COMPLETED!")
        print("✅ Page structure analysis finished")
        print("✅ Check the output above for selector recommendations")
    else:
        print("❌ ANALYSIS FAILED!")
        print("Please check the implementation and try again")
    
    print("=" * 80)
