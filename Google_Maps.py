'''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
import time

def scroll_google_maps():
    driver = uc.Chrome()
    
    try:
        # Navigate to Google Maps
        driver.get('https://www.google.com/maps/search/premium+government+hospitals+in+delhi/@28.6385655,77.0180121,11z?entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D')
        
        # Wait for initial load
        time.sleep(5)
        
        # Click the first result
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc"))
        )
        element.click()
        
        # Wait for the results panel to load
        time.sleep(3)
        
        urls = set()
        scroll_pause_time = 2
        scroll_attempts = 0
        max_attempts = 50  # Maximum number of scroll attempts
        
        while scroll_attempts < max_attempts:
            try:
                # Find the scrollable container
                scrollable_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd"))
                )
                
                # Get current scroll position
                last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                
                # Collect URLs
                places = driver.find_elements(By.CSS_SELECTOR, "a[href*='maps/place']")
                for place in places:
                    url = place.get_attribute('href')
                    if url:
                        urls.add(url)
                
                # Scroll down
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                    scrollable_div
                )
                
                # Wait for new content to load
                time.sleep(scroll_pause_time)
                
                # Calculate new scroll height
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                
                # Print progress
                print(f"Scroll attempt {scroll_attempts + 1}, Found {len(urls)} unique URLs")
                
                # If heights are the same, try a few more times before breaking
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0  # Reset counter if we successfully scrolled
                
                # Small scroll up and down to trigger loading of new content
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight - 100', 
                    scrollable_div
                )
                time.sleep(0.5)
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                    scrollable_div
                )
                
            except Exception as e:
                print(f"Scroll error: {str(e)}")
                scroll_attempts += 1
                time.sleep(1)
        
        # Print results
        print("\nAll collected URLs:")
        for url in urls:
            print(url)
        print(f"\nTotal unique URLs found: {len(urls)}")
        
    except TimeoutException:
        print("Timeout waiting for element")
    except NoSuchElementException:
        print("Element not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Save URLs to file
        try:
            with open('google_maps_urls.txt', 'w') as f:
                for url in urls:
                    f.write(url + '\n')
            print("URLs saved to google_maps_urls.txt")
        except Exception as e:
            print(f"Error saving URLs: {str(e)}")
            
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    scroll_google_maps()'''
#Pipeline -1
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
import time
import csv
import pandas as pd
import os
from urllib.parse import quote
import signal
import subprocess

# Define search terms for stationery businesses
SEARCH_TERMS = [
    # "Stationery store",
    # "Stationery shop",
    # "School supplies store",
    # "Office supplies store",
    "Bookstore",
    "General store",
    "Gift shop",
    "Notebooks",
    "Pens",
    "Pencils",
    "Geometry box",
    "Compass box",
    "Art supplies",
    "Writing materials",
    "Exam supplies",
    "Paper shop",
    "Stationery and books",
    "Stationery and gifts",
    "School stationery shop",
    "Office stationery supplier",
    "Notebooks and pens shop",
    "Stationery wholesale",
    "Stationery store near me",
    "Xerox and stationery",
    "General store stationery",
    "Book & stationery shop"
]

# Chennai pin codes (first 20 major ones)
CHENNAI_PINCODES = [
    "600001", "600002", "600003", "600004", "600005",
    "600006", "600007", "600008", "600009", "600010",
    "600011", "600012", "600013", "600014", "600015",
    "600016", "600017", "600018", "600019", "600020"
]

def safe_driver_quit(driver):
    """
    Safely quit the Chrome driver with enhanced cleanup for virtual servers.
    Uses a step-by-step approach with timeouts to prevent hanging.
    """
    if not driver:
        return

    print("Closing Chrome driver...")

    # Step 1: Close all browser windows gracefully
    try:
        windows = driver.window_handles
        for window in windows:
            try:
                driver.switch_to.window(window)
                driver.close()
            except:
                pass
        print("✓ Browser windows closed")
    except:
        print("⚠ Could not close browser windows gracefully")

    # Step 2: Quit the driver normally
    try:
        driver.quit()
        print("✓ Driver quit successfully")
        return
    except Exception as e:
        print(f"⚠ Normal quit failed: {e}")

    # Step 3: Force terminate the Chrome process
    try:
        if hasattr(driver, 'service') and driver.service and hasattr(driver.service, 'process'):
            process = driver.service.process
            if process and process.poll() is None:  # Process is still running
                print("Forcing Chrome process termination...")
                process.terminate()

                # Wait up to 10 seconds for graceful termination
                try:
                    process.wait(timeout=10)
                    print("✓ Chrome process terminated")
                    return
                except subprocess.TimeoutExpired:
                    print("⚠ Graceful termination timed out, force killing...")
                    process.kill()
                    process.wait(timeout=5)
                    print("✓ Chrome process killed")
                    return
    except Exception as e:
        print(f"⚠ Process termination failed: {e}")

    # Step 4: System-level cleanup (last resort)
    try:
        import psutil
        print("Performing system-level Chrome cleanup...")
        killed_count = 0

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    # Only kill Chrome processes that look like our webdriver instances
                    if any(keyword in cmdline.lower() for keyword in ['chromedriver', 'undetected', 'webdriver']):
                        proc.kill()
                        killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed_count > 0:
            print(f"✓ Killed {killed_count} remaining Chrome processes")
        else:
            print("✓ No remaining Chrome processes found")

    except ImportError:
        print("⚠ psutil not available for system-level cleanup")
    except Exception as e:
        print(f"⚠ System-level cleanup failed: {e}")

    print("Driver cleanup completed")

def create_stable_driver():
    """
    Create a Chrome driver optimized for virtual servers with enhanced stability
    """
    options = uc.ChromeOptions()

    # Essential stability options for virtual servers
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")

    # Memory optimization for virtual servers
    options.add_argument("--memory-pressure-off")
    options.add_argument("--max_old_space_size=2048")
    options.add_argument("--aggressive-cache-discard")

    # Performance optimization
    options.add_argument("--disable-images")  # Faster loading
    options.add_argument("--disable-javascript")  # We don't need JS for basic scraping

    # Window size for consistency
    options.add_argument("--window-size=1920,1080")

    # Uncomment the next line for headless mode (recommended for virtual servers)
    options.add_argument("--headless")

    # User agent to avoid detection
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Prefs to disable unnecessary features
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 2,
            "media_stream": 2,
        },
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2,
    }
    # options.add_experimental_option("prefs", prefs)
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)

    # Try to create driver with retries
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Creating Chrome driver (attempt {attempt + 1}/{max_retries})...")
            driver = uc.Chrome(options=options, version_main=None)

            # Test the driver with a simple page
            driver.get("about:blank")
            print("✓ Chrome driver created successfully")
            return driver

        except Exception as e:
            print(f"✗ Driver creation attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("All driver creation attempts failed")
                raise e

def scroll_google_maps_single_search(search_term, pincode):
    """
    Scrape Google Maps for a single search term and pincode combination
    """
    driver = None
    all_data = []

    try:
        driver = create_stable_driver()

        # Create search query with pincode
        search_query = f"{search_term} {pincode}"
        encoded_query = search_query.replace(" ", "+")

        # Construct Google Maps URL for Chennai area
        maps_url = f"https://www.google.com/maps/search/{encoded_query}/@12.8850351,79.835029,9.74z?entry=ttu&g_ep=EgoyMDI1MDgzMC4wIKXMDSoASAFQAw%3D%3D"

        print(f"Searching for: {search_query}")
        print(f"URL: {maps_url}")

        # Navigate to Google Maps
        driver.get(maps_url)

        # Wait for initial load with better timing
        print("Loading Google Maps...")
        time.sleep(8)

        # Click the first result to open the results panel with timeout
        print("Clicking first result to open results panel...")
        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc"))
            )
            element.click()
            print("✓ First result clicked successfully")
        except TimeoutException:
            print("⚠ Timeout waiting for first result - trying alternative approach")
            # Try to find any clickable map result
            try:
                alternative_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='maps/place'], .hfpxzc")
                if alternative_elements:
                    alternative_elements[0].click()
                    print("✓ Alternative result clicked")
                else:
                    print("✗ No clickable results found")
                    return []
            except Exception as e:
                print(f"✗ Alternative click failed: {e}")
                return []

        # Wait for the results panel to load
        print("Waiting for results panel to load...")
        time.sleep(5)

        urls = set()
        scroll_pause_time = 3  # Increased pause time for better loading
        scroll_attempts = 0
        max_attempts = 25  # Reduced for faster completion
        consecutive_no_new_content = 0
        max_consecutive_no_new = 3  # Reduced to prevent hanging

        # Add overall timeout for the entire search (5 minutes max)
        search_start_time = time.time()
        max_search_time = 300  # 5 minutes timeout

        def find_scrollable_container():
                """Try multiple selectors to find the scrollable container"""
                selectors = [
                    "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd",  # Original selector
                    "div[role='main']",  # Main content area
                    "div.siAUzd",  # Alternative container
                    "div.TFQHme",  # Another possible container
                    "div[data-value='Search results']",  # Search results container
                    ".m6QErb",  # Simplified version
                    "[role='main'] div[style*='overflow']",  # Any scrollable div in main
                ]

                for selector in selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            # Check if element is scrollable
                            scroll_height = driver.execute_script("return arguments[0].scrollHeight", element)
                            client_height = driver.execute_script("return arguments[0].clientHeight", element)
                            if scroll_height > client_height:
                                print(f"Found scrollable container with selector: {selector}")
                                return element
                    except Exception as e:
                        continue
                return None

        while scroll_attempts < max_attempts:
                try:
                    # Check for overall timeout
                    if time.time() - search_start_time > max_search_time:
                        print(f"⏰ Search timeout reached ({max_search_time/60:.1f} minutes). Stopping search.")
                        break

                    # Find the scrollable container using multiple strategies
                    scrollable_div = find_scrollable_container()

                    if not scrollable_div:
                        print("Could not find scrollable container, trying alternative approach...")
                        # Fallback: scroll the entire page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(scroll_pause_time)
                        scroll_attempts += 1
                        continue

                    # Store current URL count
                    previous_url_count = len(urls)

                    # Get current scroll position
                    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

                    # Collect URLs and other data
                    places = driver.find_elements(By.CSS_SELECTOR, "a[href*='maps/place']")
                    for place in places:
                        try:
                            url = place.get_attribute('href')
                            if url and url not in urls:
                                urls.add(url)
                                # Add search context to the data
                                place_data = {
                                    'URL': url,
                                    'Search_Term': search_term,
                                    'Pincode': pincode,
                                    'Search_Query': f"{search_term} {pincode}"
                                }
                                all_data.append(place_data)
                        except Exception as e:
                            continue

                    # Multiple scrolling strategies
                    # Strategy 1: Scroll to bottom
                    driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight',
                        scrollable_div
                    )
                    time.sleep(1)

                    # Strategy 2: Gradual scrolling to trigger lazy loading
                    current_scroll = driver.execute_script("return arguments[0].scrollTop", scrollable_div)
                    scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

                    # Scroll in smaller increments
                    for i in range(3):
                        new_scroll_pos = current_scroll + (scroll_height - current_scroll) // 3 * (i + 1)
                        driver.execute_script(f"arguments[0].scrollTop = {new_scroll_pos}", scrollable_div)
                        time.sleep(0.5)

                    # Wait for new content to load
                    time.sleep(scroll_pause_time)

                    # Calculate new scroll height
                    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

                    # Check if we found new URLs
                    new_url_count = len(urls)
                    new_urls_found = new_url_count - previous_url_count

                    # Print progress
                    print(f"Scroll attempt {scroll_attempts + 1}, Found {new_url_count} unique URLs (+{new_urls_found} new)")

                    # Update counters based on progress
                    if new_height == last_height and new_urls_found == 0:
                        consecutive_no_new_content += 1
                        scroll_attempts += 1
                    else:
                        consecutive_no_new_content = 0
                        if new_urls_found > 0:
                            scroll_attempts = max(0, scroll_attempts - 1)  # Reset counter if we found new content

                    # Stop if we haven't found new content for several attempts
                    if consecutive_no_new_content >= max_consecutive_no_new:
                        print(f"No new content found for {max_consecutive_no_new} consecutive attempts. Stopping.")
                        break

                    # Strategy 3: Small scroll up and down to trigger loading of new content
                    driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight - 200',
                        scrollable_div
                    )
                    time.sleep(0.5)
                    driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight',
                        scrollable_div
                    )
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Scroll error: {str(e)}")
                    scroll_attempts += 1
                    time.sleep(2)

        # Print the complete list of URLs for this search
        print(f"\nComplete list of URLs for '{search_term} {pincode}':")
        for data in all_data:
            print(data['URL'])
        print(f"\nTotal unique URLs found for this search: {len(urls)}")

        # Return the list of data
        return all_data

    except TimeoutException:
        print("Timeout waiting for element")
    except NoSuchElementException:
        print("Element not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        safe_driver_quit(driver)

    return []

def get_individual_csv_filename(search_term):
    """
    Generate filename for individual search term CSV
    """
    safe_search_term = "".join(c for c in search_term if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_search_term = safe_search_term.replace(' ', '_').lower()
    return f"{safe_search_term}_results.csv"

def append_to_individual_csv(data_list, search_term):
    """
    Append search results to individual CSV file for a specific search term
    Creates file with header if it doesn't exist, otherwise appends data
    """
    if not data_list:
        return 0

    csv_filename = get_individual_csv_filename(search_term)
    file_exists = os.path.exists(csv_filename)

    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['URL', 'Search_Term', 'Pincode', 'Search_Query']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        writer.writerows(data_list)

    print(f"Appended {len(data_list)} results to {csv_filename}")
    return len(data_list)

def append_to_master_csv(data_list, csv_filename='stationery_shops_chennai_master.csv'):
    """
    Append data to master CSV file, avoiding duplicates
    Optimized for real-time incremental updates
    """
    if not data_list:
        return 0

    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(csv_filename)

    # Read existing URLs to avoid duplicates (only if file exists and is not empty)
    existing_urls = set()
    if file_exists:
        try:
            with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_urls.add(row['URL'])
        except Exception as e:
            print(f"Warning: Error reading existing master CSV: {e}")

    # Filter out duplicates
    new_data = []
    for item in data_list:
        if item['URL'] not in existing_urls:
            new_data.append(item)
            existing_urls.add(item['URL'])

    # Append new data to CSV
    if new_data:
        with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['URL', 'Search_Term', 'Pincode', 'Search_Query']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header only if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerows(new_data)

        print(f"Added {len(new_data)} new unique entries to master CSV")
    else:
        print("No new unique entries to add to master CSV")

    return len(new_data)

def scroll_google_maps_multiple_searches():
    """
    Main function to search for all stationery terms with all pin codes
    NEW BEHAVIOR: Real-time incremental data saving after each individual search
    """
    total_results = 0
    total_new_results = 0
    total_searches = len(SEARCH_TERMS) * len(CHENNAI_PINCODES)
    current_search = 0

    print(f"Starting comprehensive search for stationery shops in Chennai")
    print(f"REAL-TIME INCREMENTAL SAVING MODE")
    print(f"Total searches to perform: {total_searches}")
    print(f"Search terms: {len(SEARCH_TERMS)}")
    print(f"Pin codes: {len(CHENNAI_PINCODES)}")
    print(f"Results will be saved immediately after each search")
    print("-" * 80)

    # Process each search term across all pin codes
    for search_term_index, search_term in enumerate(SEARCH_TERMS, 1):
        print(f"\n{'='*80}")
        print(f"PROCESSING SEARCH TERM {search_term_index}/{len(SEARCH_TERMS)}: '{search_term}'")
        print(f"{'='*80}")

        search_term_total_results = 0  # Track results for this search term

        # Process this search term across all pin codes
        for pincode_index, pincode in enumerate(CHENNAI_PINCODES, 1):
            current_search += 1
            print(f"\n[{current_search}/{total_searches}] Processing: {search_term} in {pincode}")
            print(f"Pin code {pincode_index}/{len(CHENNAI_PINCODES)} for search term '{search_term}'")

            try:
                # Perform single search
                results = scroll_google_maps_single_search(search_term, pincode)

                if results:
                    # REAL-TIME SAVING: Immediately save results to both CSV files
                    print(f"Found {len(results)} results. Saving immediately...")

                    # 1. Append to individual CSV for this search term
                    individual_new_count = append_to_individual_csv(results, search_term)

                    # 2. Append to master CSV
                    master_new_count = append_to_master_csv(results)

                    # Update counters
                    search_term_total_results += len(results)
                    total_results += len(results)
                    total_new_results += master_new_count

                    print(f"✅ Saved: {individual_new_count} to individual CSV, {master_new_count} new to master CSV")
                else:
                    print(f"No results found for {search_term} in {pincode}")

                # Add delay between searches to avoid being blocked
                if current_search < total_searches:
                    print("Waiting 10 seconds before next search...")
                    time.sleep(10)

            except Exception as e:
                print(f"❌ Error in search '{search_term} {pincode}': {e}")
                print("Continuing to next search...")
                continue

        # After processing all pin codes for this search term:
        print(f"\n{'-'*60}")
        print(f"COMPLETED SEARCH TERM: '{search_term}'")
        print(f"Total results found: {search_term_total_results}")
        individual_csv_filename = get_individual_csv_filename(search_term)
        print(f"Individual CSV: {individual_csv_filename}")
        print(f"{'-'*60}")

        print(f"Completed {search_term_index}/{len(SEARCH_TERMS)} search terms")

    # Final summary - no need to create master CSV as it was built incrementally
    print(f"\n{'='*80}")
    print(f"SEARCH COMPLETED!")
    print(f"{'='*80}")

    # Count total lines in master CSV to show final statistics
    master_csv_filename = 'stationery_shops_chennai_master.csv'
    total_unique_results = 0
    if os.path.exists(master_csv_filename):
        try:
            with open(master_csv_filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                total_unique_results = sum(1 for row in reader)
        except Exception as e:
            print(f"Warning: Could not count master CSV rows: {e}")

    print(f"Total searches performed: {current_search}")
    print(f"Total results found: {total_results}")
    print(f"Total unique results in master CSV: {total_unique_results}")
    print(f"Total new unique results added: {total_new_results}")
    print(f"Individual CSV files created: {len(SEARCH_TERMS)} files")
    print(f"Master CSV file: {master_csv_filename}")
    print(f"\n📁 Files created:")

    # List all individual CSV files created
    for search_term in SEARCH_TERMS:
        individual_csv = get_individual_csv_filename(search_term)
        if os.path.exists(individual_csv):
            try:
                with open(individual_csv, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    count = sum(1 for row in reader)
                print(f"  ✅ {individual_csv} ({count} results)")
            except:
                print(f"  ✅ {individual_csv}")

    print(f"  ✅ {master_csv_filename} ({total_unique_results} unique results)")
    print("="*80)

    return total_new_results

if __name__ == "__main__":
    # Execute the comprehensive scraping
    total_new_results = scroll_google_maps_multiple_searches()
