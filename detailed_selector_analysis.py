#!/usr/bin/env python3
"""
Detailed selector analysis to find exact working selectors
"""

import sys
import os
import time
import re
from selenium.webdriver.common.by import By

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Extract_Maps import create_chrome_driver, safe_driver_quit

def detailed_selector_analysis(url):
    """Get detailed selector information for each field"""
    print(f"🔍 Detailed Selector Analysis for:")
    print(f"URL: {url}")
    print("=" * 80)
    
    driver = None
    try:
        driver = create_chrome_driver(thread_id=999)
        
        if driver:
            driver.get(url)
            time.sleep(8)
            
            # Scroll to load all elements
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            print("\n📊 DETAILED ELEMENT ANALYSIS")
            print("=" * 50)
            
            # 1. Store Type Analysis
            print("\n🏪 STORE TYPE - DETAILED ANALYSIS")
            print("-" * 40)
            find_store_type_selectors(driver)
            
            # 2. Rating Analysis
            print("\n⭐ RATING - DETAILED ANALYSIS")
            print("-" * 40)
            find_rating_selectors(driver)
            
            # 3. Operating Hours Analysis
            print("\n🕒 OPERATING HOURS - DETAILED ANALYSIS")
            print("-" * 40)
            find_operating_hours_selectors(driver)
            
            # 4. Phone Analysis
            print("\n📞 PHONE - DETAILED ANALYSIS")
            print("-" * 40)
            find_phone_selectors(driver)
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if driver:
            safe_driver_quit(driver)

def find_store_type_selectors(driver):
    """Find working selectors for store type"""
    try:
        # Test current selectors
        current_selectors = [
            "//button[contains(@class, 'DkEaL') and contains(@jsaction, 'category')]",
            "//button[contains(@class, 'DkEaL')]",
            "//span[contains(@class, 'YhemCb')]"
        ]
        
        print("Testing current selectors:")
        for selector in current_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                print(f"  {selector}: Found {len(elements)} elements")
                for i, elem in enumerate(elements[:3]):
                    text = elem.text.strip()
                    if text:
                        print(f"    [{i}] Text: '{text}'")
            except Exception as e:
                print(f"  {selector}: Error - {e}")
        
        # Look for alternative selectors
        print("\nLooking for alternative selectors:")
        
        # Check all buttons with text
        buttons = driver.find_elements(By.TAG_NAME, "button")
        category_buttons = []
        for button in buttons:
            try:
                text = button.text.strip()
                classes = button.get_attribute("class")
                if text and any(keyword in text.lower() for keyword in ['institute', 'academy', 'center', 'coaching', 'education']):
                    category_buttons.append({
                        'text': text,
                        'classes': classes,
                        'xpath': f"//button[contains(text(), '{text}')]"
                    })
            except:
                continue
        
        if category_buttons:
            print("  ✅ Found category buttons:")
            for btn in category_buttons[:3]:
                print(f"    Text: '{btn['text']}'")
                print(f"    Classes: {btn['classes']}")
                print(f"    Suggested XPath: {btn['xpath']}")
        else:
            print("  ❌ No category buttons found")
            
    except Exception as e:
        print(f"Error in store type analysis: {e}")

def find_rating_selectors(driver):
    """Find working selectors for rating"""
    try:
        # Test current selectors
        current_selectors = [
            "//div[contains(@class, 'F7nice')]//span[@aria-hidden='true']",
            "//span[contains(@class, 'ceNzKf')]/preceding-sibling::span[@aria-hidden='true']",
            "//div[contains(@jslog, '76333')]//span[@aria-hidden='true']"
        ]
        
        print("Testing current selectors:")
        for selector in current_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                print(f"  {selector}: Found {len(elements)} elements")
                for i, elem in enumerate(elements[:3]):
                    text = elem.text.strip()
                    if text:
                        print(f"    [{i}] Text: '{text}'")
            except Exception as e:
                print(f"  {selector}: Error - {e}")
        
        # Look for rating patterns
        print("\nLooking for rating patterns:")
        all_spans = driver.find_elements(By.TAG_NAME, "span")
        rating_spans = []
        
        for span in all_spans:
            try:
                text = span.text.strip()
                if re.match(r'^[0-5]\.[0-9]$', text):
                    classes = span.get_attribute("class")
                    aria_hidden = span.get_attribute("aria-hidden")
                    parent_classes = span.find_element(By.XPATH, "..").get_attribute("class")
                    
                    rating_spans.append({
                        'text': text,
                        'classes': classes,
                        'aria_hidden': aria_hidden,
                        'parent_classes': parent_classes
                    })
            except:
                continue
        
        if rating_spans:
            print("  ✅ Found rating spans:")
            for rating in rating_spans[:3]:
                print(f"    Text: '{rating['text']}'")
                print(f"    Classes: {rating['classes']}")
                print(f"    Aria-hidden: {rating['aria_hidden']}")
                print(f"    Parent classes: {rating['parent_classes']}")
                
                # Suggest XPath
                if rating['aria_hidden'] == 'true':
                    print(f"    Suggested XPath: //span[@aria-hidden='true' and text()='{rating['text']}']")
                else:
                    print(f"    Suggested XPath: //span[text()='{rating['text']}']")
        else:
            print("  ❌ No rating spans found")
            
    except Exception as e:
        print(f"Error in rating analysis: {e}")

def find_operating_hours_selectors(driver):
    """Find working selectors for operating hours"""
    try:
        # Test current selectors
        current_selectors = [
            "//span[contains(@class, 'ZDu9vd')]",
            "//div[contains(@class, 'MkV9')]//span[contains(@class, 'ZDu9vd')]"
        ]
        
        print("Testing current selectors:")
        for selector in current_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                print(f"  {selector}: Found {len(elements)} elements")
                for i, elem in enumerate(elements[:3]):
                    text = elem.text.strip()
                    if text:
                        print(f"    [{i}] Text: '{text}'")
            except Exception as e:
                print(f"  {selector}: Error - {e}")
        
        # Look for hours-related elements
        print("\nLooking for hours-related elements:")
        hours_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Open') or contains(text(), 'Closed') or contains(text(), 'pm') or contains(text(), 'am')]")
        
        hours_candidates = []
        for elem in hours_elements:
            try:
                text = elem.text.strip()
                tag_name = elem.tag_name
                classes = elem.get_attribute("class")
                
                if text and len(text) < 50:
                    hours_candidates.append({
                        'text': text,
                        'tag': tag_name,
                        'classes': classes
                    })
            except:
                continue
        
        if hours_candidates:
            print("  ✅ Found hours candidates:")
            for hours in hours_candidates[:5]:
                print(f"    Text: '{hours['text']}'")
                print(f"    Tag: {hours['tag']}, Classes: {hours['classes']}")
        else:
            print("  ❌ No hours candidates found")
            
    except Exception as e:
        print(f"Error in operating hours analysis: {e}")

def find_phone_selectors(driver):
    """Find working selectors for phone numbers"""
    try:
        # Look for phone patterns
        print("Looking for phone number patterns:")
        
        # Search for elements containing phone patterns
        phone_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '098') or contains(text(), '091') or contains(text(), '+91')]")
        
        phone_candidates = []
        for elem in phone_elements:
            try:
                text = elem.text.strip()
                tag_name = elem.tag_name
                classes = elem.get_attribute("class")
                
                # Check if it looks like a phone number
                if re.search(r'\d{10}|\d{3}[-\s]\d{3}[-\s]\d{4}|\+91[-\s]?\d{10}', text):
                    phone_candidates.append({
                        'text': text,
                        'tag': tag_name,
                        'classes': classes
                    })
            except:
                continue
        
        if phone_candidates:
            print("  ✅ Found phone candidates:")
            for phone in phone_candidates[:3]:
                print(f"    Text: '{phone['text']}'")
                print(f"    Tag: {phone['tag']}, Classes: {phone['classes']}")
        else:
            print("  ❌ No phone candidates found")
            
    except Exception as e:
        print(f"Error in phone analysis: {e}")

if __name__ == "__main__":
    # Test with a URL from the CSV file
    test_url = "https://www.google.com/maps/place/EDIA/data=!4m7!3m6!1s0x390cfb3e3f468a1d:0xa20aa5a10c9de3f7!8m2!3d28.6822709!4d77.3127341!16s%2Fg%2F11fmlwl3fp!19sChIJHYpGPz77DDkR9-OdDKGlCqI?authuser=0&hl=en&rclk=1"
    
    print("🚀 Starting Detailed Selector Analysis")
    print("=" * 80)
    
    success = detailed_selector_analysis(test_url)
    
    print("\n" + "=" * 80)
    print("📊 ANALYSIS COMPLETE")
    print("=" * 80)
