
    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import csv
import pandas as pd
import re
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

# Try to import webdriver_manager for automatic ChromeDriver management
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("webdriver-manager not available. Install it with: pip install webdriver-manager")

# Global lock for thread-safe CSV writing
csv_lock = threading.Lock()

def get_chrome_version():
    """Get the installed Chrome browser version for better compatibility"""
    try:
        # Try different methods to get Chrome version
        methods = [
            # Windows
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            # Alternative Windows method
            r'powershell "Get-ItemProperty HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion | Where-Object {$_.DisplayName -like \"*Chrome*\"}"',
        ]

        for method in methods:
            try:
                result = subprocess.run(method, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout:
                    # Extract version number from output
                    version_match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', result.stdout)
                    if version_match:
                        major_version = int(version_match.group(1))
                        return major_version
            except:
                continue

        # Fallback: Try to get version from Chrome executable
        import platform
        if platform.system() == "Windows":
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10)
                        version_match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', result.stdout)
                        if version_match:
                            return int(version_match.group(1))
                    except:
                        continue

    except Exception as e:
        print(f"Warning: Could not detect Chrome version: {e}")

    return None

def extract_coordinates_from_url(url):
    """
    Extract latitude and longitude coordinates from Google Maps URL

    Args:
        url (str): Google Maps URL containing coordinates

    Returns:
        tuple: (latitude, longitude) as strings, or ("Not Found", "Not Found") if not found
    """
    try:
        # Use regex to find latitude (3d parameter) and longitude (4d parameter)
        lat_pattern = r'3d([+-]?\d+\.?\d*)'
        lng_pattern = r'4d([+-]?\d+\.?\d*)'

        lat_match = re.search(lat_pattern, url)
        lng_match = re.search(lng_pattern, url)

        latitude = lat_match.group(1) if lat_match else "Not Found"
        longitude = lng_match.group(1) if lng_match else "Not Found"

        return latitude, longitude

    except Exception as e:
        print(f"Error extracting coordinates from URL: {str(e)}")
        return "Not Found", "Not Found"

def safe_driver_quit(driver):
    """Safely quit the Chrome driver with error handling"""
    if not driver:
        return

    try:
        # First try to close all windows
        try:
            driver.close()
        except:
            pass

        # Then quit the driver
        driver.quit()
    except (OSError, Exception) as e:
        print(f"Warning: Error during driver.quit(): {e}")
        try:
            # Try to terminate the process directly
            if hasattr(driver, 'service') and driver.service and hasattr(driver.service, 'process') and driver.service.process:
                driver.service.process.terminate()
                driver.service.process.wait(timeout=5)
        except Exception as e2:
            print(f"Warning: Error terminating process: {e2}")
            try:
                # Force kill as last resort
                if hasattr(driver, 'service') and driver.service and hasattr(driver.service, 'process') and driver.service.process:
                    driver.service.process.kill()
            except:
                pass

def append_result_to_csv(result, output_filename, write_header=False):
    """
    Thread-safe append of a single result to the output CSV file immediately
    """
    try:
        with csv_lock:  # Thread-safe CSV writing
            with open(output_filename, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['URL', 'Name', 'Address', 'Website', 'Phone', 'Latitude', 'Longitude']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header only if this is the first write
                if write_header:
                    writer.writeheader()

                # Write the data row
                writer.writerow(result)

        return True
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return False

def check_url_already_processed(url, output_filename):
    """
    Check if a URL has already been processed by reading the existing output file
    """
    if not os.path.exists(output_filename):
        return False

    try:
        with open(output_filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('URL') == url:
                    return True
    except Exception as e:
        print(f"Warning: Error checking processed URLs: {e}")

    return False

def scroll_page(driver):
    """
    Scroll the page to help reveal dynamic content
    """
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Scroll in increments
    for i in range(0, total_height, 500):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)
    
    # Scroll back to top
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def extract_phone_number(driver, wait):
    # Scroll the page first
    scroll_page(driver)
    
    phone_xpaths = [
        "//div[contains(@class, 'fontBodyMedium') and contains(text(), '0')]",
        "//div[contains(@class, 'Io6YTe') and contains(text(), '0')]",
        "//div[contains(@class, 'fontBodyMedium kR99db')]",
        "//div[contains(@class, 'rogA2c')]//div[contains(@class, 'Io6YTe')]",
        "//div[contains(@class, 'phone-number')]",
        "//a[contains(@href, 'tel:')]"
    ]
    
    for xpath in phone_xpaths:
        try:
            # Try to find the elements
            phone_elements = driver.find_elements(By.XPATH, xpath)
            
            for element in phone_elements:
                # Scroll to the element to ensure it's in view
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                # Extract text
                phone_text = element.text.strip()
                
                # Modified regex pattern to capture longer phone numbers (using raw string)
                phone_match = re.findall(r'(?:\+?\d{1,4}[-.\s]?)?\d{3,}[-.\s]?\d{3,}[-.\s]?\d{3,}', phone_text)
                
                if phone_match:
                    # Clean the phone number but preserve the country code if present
                    phone_number = phone_match[0]
                    # Remove spaces and common separators but keep the plus sign if present
                    cleaned_number = ''.join(c for c in phone_number if c.isdigit() or c == '+')
                    return cleaned_number
        
        except Exception as e:
            print(f"Error searching for phone number: {str(e)}")
    
    return "Phone Number Not Found"


def scrape_data(url, driver, wait):
    try:
        # Navigate to the URL
        driver.get(url)
        time.sleep(3)  # Give some time for the page to load
        
        # Scroll the page
        scroll_page(driver)
        
        # Initialize variables with default values
        address = website = phone = "Not Found"
        
        try:
            # Address extraction
            address_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'rogA2c')]/div[contains(@class,'Io6YTe')]")
            ))
            # Scroll to address element
            driver.execute_script("arguments[0].scrollIntoView(true);", address_element)
            address = address_element.text
        except (TimeoutException, NoSuchElementException):
            pass

        try:
            # Website extraction
            website_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@aria-label, 'Website')]")
            ))
            website = website_element.get_attribute("href")
        except (TimeoutException, NoSuchElementException):
            
            pass
        try:
            name_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(@class, 'DUwDvf lfPIob')]")
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", name_element)
            name = name_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            name = "Name Not Found"

       

        # Phone number extraction
        phone = extract_phone_number(driver, wait)

        # Coordinate extraction from URL
        latitude, longitude = extract_coordinates_from_url(url)

        return {
            'URL': url,
            'Name': name,
            'Address': address,
            'Website': website,
            'Phone': phone,
            'Latitude': latitude,
            'Longitude': longitude
        }

    except WebDriverException as e:
        print(f"Error processing URL {url}: {str(e)}")
        # Even if scraping fails, we can still extract coordinates from the URL
        latitude, longitude = extract_coordinates_from_url(url)
        return {
            'URL': url,
            'Name': 'Error',
            'Address': 'Error',
            'Website': 'Error',
            'Phone': 'Error',
            'Latitude': latitude,
            'Longitude': longitude
        }

def main():
    # Check if the input CSV file exists
    input_filename = 'Delhi_coaching.csv'
    if not os.path.exists(input_filename):
        print(f"Error: Input file '{input_filename}' not found!")
        print("Please make sure you have run the Google_Maps.py script first to generate the master CSV file.")
        print("The file should be created by the Google Maps scraper with the correct spelling: 'stationery' not 'stationary'")
        return

    # Read URLs from CSV file
    try:
        df = pd.read_csv(input_filename)
        if 'URL' not in df.columns:
            print(f"Error: 'URL' column not found in {input_filename}")
            print(f"Available columns: {list(df.columns)}")
            return

        urls = df['URL'].tolist()
        print(f"Successfully loaded {len(urls)} URLs from {input_filename}")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return

    # Setup output file for real-time incremental writing
    output_filename = 'Delhi_coaching_output.csv'

    # Check if output file already exists to determine if we need to write header
    file_exists = os.path.exists(output_filename)

    # Count existing processed URLs for resume capability
    processed_count = 0
    if file_exists:
        try:
            with open(output_filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                processed_count = sum(1 for row in reader)
            print(f"Found existing output file with {processed_count} processed URLs")
            print("Will skip already processed URLs and continue from where left off")
        except Exception as e:
            print(f"Warning: Error reading existing output file: {e}")

    # Continue with multithreaded processing
    process_urls_multithreaded(urls, output_filename, file_exists)

def process_urls_multithreaded(urls, output_filename, file_exists):
    """
    Process URLs using multithreading for improved performance
    """
    # Multithreading configuration
    MAX_THREADS = 2  # Conservative number to avoid overwhelming Google Maps

    # Counters for real-time progress tracking
    total_urls = len(urls)
    processed_new = 0
    skipped_existing = 0
    errors = 0

    print(f"\n{'='*80}")
    print(f"STARTING MULTITHREADED REAL-TIME INCREMENTAL DATA EXTRACTION")
    print(f"{'='*80}")
    print(f"Total URLs to process: {total_urls}")
    print(f"Output file: {output_filename}")
    print(f"Threads: {MAX_THREADS}")
    print(f"Mode: Real-time incremental CSV writing with coordinates")
    print("-" * 80)

    # Write header if file doesn't exist
    if not file_exists:
        try:
            with open(output_filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['URL', 'Name', 'Address', 'Website', 'Phone', 'Latitude', 'Longitude']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            print("✅ Created output file with headers")
        except Exception as e:
            print(f"❌ Error creating output file: {e}")
            return

    try:
        # Process URLs using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            # Submit all URL processing tasks
            future_to_url = {}
            for index, url in enumerate(urls, 1):
                future = executor.submit(process_single_url, url, output_filename,
                                       index % MAX_THREADS, total_urls, index)
                future_to_url[future] = (url, index)

            # Process completed tasks
            for future in as_completed(future_to_url):
                url, index = future_to_url[future]
                try:
                    result = future.result()

                    if result['status'] == 'success':
                        processed_new += 1
                    elif result['status'] == 'skipped':
                        skipped_existing += 1
                    else:
                        errors += 1

                    # Progress update
                    completed = processed_new + skipped_existing + errors
                    print(f"📊 Progress: {completed}/{total_urls} | New: {processed_new} | Skipped: {skipped_existing} | Errors: {errors}")

                except Exception as e:
                    errors += 1
                    print(f"❌ Thread execution error for {url}: {str(e)}")

    except KeyboardInterrupt:
        print(f"\n⚠️  Script interrupted by user")
        print(f"✅ Progress saved: {processed_new} URLs processed and saved to {output_filename}")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print(f"✅ Progress saved: {processed_new} URLs processed and saved to {output_filename}")

    finally:
        # Final summary
        print(f"\n{'='*80}")
        print(f"MULTITHREADED EXTRACTION COMPLETED!")
        print(f"{'='*80}")
        print(f"Total URLs: {total_urls}")
        print(f"New URLs processed: {processed_new}")
        print(f"Already existing (skipped): {skipped_existing}")
        print(f"Errors encountered: {errors}")
        print(f"Output file: {output_filename}")
        print(f"Threads used: {MAX_THREADS}")

        # Count final records in output file
        try:
            if os.path.exists(output_filename):
                with open(output_filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    final_count = sum(1 for _ in reader)
                print(f"Total records in output file: {final_count}")
            else:
                print(f"No output file created")
        except Exception as e:
            print(f"Warning: Could not count final records: {e}")

        print("="*80)

def create_chrome_driver(thread_id=0):
    """
    Create a Chrome driver with improved version compatibility and thread safety using standard Selenium
    """
    # Detect Chrome version for better compatibility
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"🔍 Detected Chrome version: {chrome_version}")

    def create_chrome_options(thread_id, suffix=""):
        """Create fresh Chrome options to avoid reuse errors"""
        options = ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        #options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        #options.add_argument('--disable-plugins')
        #options.add_argument('--disable-images')
        #options.add_argument('--disable-javascript')
        # Use Windows-compatible temp directory path
        temp_profile = f"C:\\temp\\chrome_profile_{thread_id}_{suffix}_{int(time.time())}"
        options.add_argument(f'--user-data-dir={temp_profile}')
        return options

    driver = None

    # Method 1: Try with webdriver-manager for automatic version management
    if WEBDRIVER_MANAGER_AVAILABLE:
        try:
            print(f"🔄 [Thread {thread_id}] Trying webdriver-manager for automatic ChromeDriver management...")
            service = Service(ChromeDriverManager().install())
            options = create_chrome_options(thread_id, "webdriver_manager")
            driver = webdriver.Chrome(service=service, options=options)
            print(f"✅ [Thread {thread_id}] Successfully created Chrome driver using webdriver-manager")
            return driver
        except Exception as e:
            print(f"❌ [Thread {thread_id}] webdriver-manager failed: {e}")

    # Method 2: Try with system ChromeDriver (if available in PATH)
    if driver is None:
        try:
            print(f"🔄 [Thread {thread_id}] Trying system ChromeDriver...")
            options = create_chrome_options(thread_id, "system")
            driver = webdriver.Chrome(options=options)
            print(f"✅ [Thread {thread_id}] Successfully created Chrome driver using system ChromeDriver")
            return driver
        except Exception as e:
            print(f"❌ [Thread {thread_id}] System ChromeDriver failed: {e}")

    # Method 3: Try with explicit ChromeDriver service (fallback)
    if driver is None:
        try:
            print(f"🔄 [Thread {thread_id}] Trying explicit ChromeDriver service...")
            options = create_chrome_options(thread_id, "explicit")
            # Try to find ChromeDriver in common locations
            possible_paths = [
                "chromedriver.exe",
                "C:\\chromedriver\\chromedriver.exe",
                "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
            ]

            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        service = Service(path)
                        driver = webdriver.Chrome(service=service, options=options)
                        print(f"✅ [Thread {thread_id}] Successfully created Chrome driver using {path}")
                        return driver
                except Exception:
                    continue

            # If no specific path works, try without service
            driver = webdriver.Chrome(options=options)
            print(f"✅ [Thread {thread_id}] Successfully created Chrome driver with default service")
            return driver

        except Exception as e:
            print(f"❌ [Thread {thread_id}] Explicit ChromeDriver service failed: {e}")

    # If all methods failed
    if driver is None:
        print(f"\n🔧 [Thread {thread_id}] ALL METHODS FAILED - SOLUTION SUGGESTIONS:")
        print("1. Update Chrome browser: chrome://settings/help")
        print("2. Install/update webdriver-manager: pip install --upgrade webdriver-manager")
        print("3. Download ChromeDriver from: https://chromedriver.chromium.org/downloads")
        print("4. Ensure ChromeDriver is in your PATH or place chromedriver.exe in the script directory")
        raise Exception("Failed to create Chrome driver with all methods")

    return driver

def process_single_url(url, output_filename, thread_id, total_urls, current_index):
    """
    Process a single URL in a thread-safe manner
    """
    driver = None
    try:
        print(f"\n[Thread {thread_id}] [{current_index}/{total_urls}] Processing URL: {url}")

        # Check if this URL was already processed (thread-safe check)
        if check_url_already_processed(url, output_filename):
            print(f"[Thread {thread_id}] ⏭️  Skipping - already processed")
            return {'status': 'skipped', 'url': url}

        # Create driver for this thread
        driver = create_chrome_driver(thread_id)
        wait = WebDriverWait(driver, 15)

        # Extract data from the URL
        result = scrape_data(url, driver, wait)

        # Thread-safe CSV writing
        success = append_result_to_csv(result, output_filename, write_header=False)

        if success:
            print(f"[Thread {thread_id}] ✅ Extracted and saved: {result.get('Name', 'N/A')}")
            print(f"[Thread {thread_id}]    Address: {result.get('Address', 'N/A')[:50]}...")
            print(f"[Thread {thread_id}]    Phone: {result.get('Phone', 'N/A')}")
            print(f"[Thread {thread_id}]    Coordinates: {result.get('Latitude', 'N/A')}, {result.get('Longitude', 'N/A')}")
            return {'status': 'success', 'url': url, 'result': result}
        else:
            print(f"[Thread {thread_id}] ❌ Failed to save result to CSV")
            return {'status': 'csv_error', 'url': url}

    except Exception as e:
        print(f"[Thread {thread_id}] ❌ Error processing URL: {str(e)}")

        # Still try to save an error record with coordinates
        try:
            latitude, longitude = extract_coordinates_from_url(url)
            error_result = {
                'URL': url,
                'Name': 'Error',
                'Address': 'Error',
                'Website': 'Error',
                'Phone': 'Error',
                'Latitude': latitude,
                'Longitude': longitude
            }
            append_result_to_csv(error_result, output_filename, write_header=False)
        except:
            pass

        return {'status': 'error', 'url': url, 'error': str(e)}

    finally:
        # Clean up driver
        if driver:
            safe_driver_quit(driver)



if __name__ == "__main__":
    main()
    
    

    
