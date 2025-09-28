'''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
import time
import csv
import pandas as pd
import re

def extract_phone_number(driver, wait):
    phone_xpaths = [
        # Try different potential phone number locations
        "//div[contains(@class, 'fontBodyMedium') and contains(text(), '0')]",
        "//div[contains(@class, 'Io6YTe') and contains(text(), '0')]",
        "//div[contains(@class, 'fontBodyMedium kR99db')]",
        "//div[contains(@class, 'rogA2c')]//div[contains(@class, 'Io6YTe')]"
    ]
    
    for xpath in phone_xpaths:
        try:
            # Try to find the element
            phone_elements = driver.find_elements(By.XPATH, xpath)
            
            for element in phone_elements:
                # Extract text
                phone_text = element.text.strip()
                
                # Use regex to extract phone number (using raw string to avoid SyntaxWarning)
                phone_match = re.findall(r'\d{3,}[-\s]?\d{3,}[-\s]?\d{3,}', phone_text)
                
                if phone_match:
                    # Return the first matched phone number
                    return phone_match[0].replace(' ', '').replace('-', '')
        
        except Exception as e:
            print(f"Error searching for phone number: {str(e)}")
    
    return "Phone Number Not Found"

def scrape_data(url, driver, wait):
    try:
        # Navigate to the URL
        driver.get(url)
        time.sleep(3)  # Give some time for the page to load
        
        # Initialize variables with default values
        address = website = phone = "Not Found"
        
        try:
            # Address extraction
            address_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'rogA2c')]/div[contains(@class,'Io6YTe')]")
            ))
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

        # Phone number extraction
        phone = extract_phone_number(driver, wait)

        return {
            'URL': url,
            'Address': address,
            'Website': website,
            'Phone': phone
        }
    except WebDriverException as e:
        print(f"Error processing URL {url}: {str(e)}")
        return {
            'URL': url,
            'Address': 'Error',
            'Website': 'Error',
            'Phone': 'Error'
        }

def main():
    # Read URLs from CSV file
    try:
        df = pd.read_csv('Project4_alt.csv')  # Replace 'input.csv' with your CSV file name
        urls = df['URL'].tolist()  # Assuming 'URL' is the column name
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return

    # Initialize the driver
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)
    
    # List to store results
    results = []

    try:
        # Process each URL
        for url in urls:
            print(f"Processing URL: {url}")
            result = scrape_data(url, driver, wait)
            results.append(result)
            time.sleep(2)  # Add delay between requests
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the driver
        driver.quit()
        
        # Save results to CSV
        try:
            df_results = pd.DataFrame(results)
            df_results.to_csv('Project_output.csv', index=False)
            print("Results saved to output.csv")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    main()'''
    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import time
import csv
import pandas as pd
import re
import os

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
    Append a single result to the output CSV file immediately
    """
    try:
        with open(output_filename, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['URL', 'Name', 'Address', 'Website', 'Phone']
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
'''def extract_phone_number(driver, wait):
    # Scroll the page first
    scroll_page(driver)
    
    try:
        # Try the most reliable XPath first - looking for elements with phone icon
        phone_elements = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Phone:')]")
        if phone_elements:
            for element in phone_elements:
                phone_text = element.get_attribute("aria-label")
                if phone_text:
                    # Extract just the number part after "Phone: "
                    phone_number = phone_text.split("Phone:")[1].strip()
                    return phone_number.replace(" ", "")
        
        # Alternative approach - look for elements with telephone numbers in the text
        phone_xpaths = [
            "//button[contains(@data-item-id, 'phone:')]",
            "//div[contains(@class, 'Io6YTe')][./parent::div[contains(@class, 'rogA2c')]][./parent::div/div/span[contains(@class, 'NhBTye')]]",
            "//span[contains(@class, 'NhBTye')]/parent::div/following-sibling::div//div[contains(@class, 'Io6YTe')]"
        ]
        
        for xpath in phone_xpaths:
            elements = driver.find_elements(By.XPATH, xpath)
            for element in elements:
                # Scroll to the element to ensure it's in view
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                phone_text = element.text.strip()
                # Check if this looks like a phone number (using raw string)
                if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{5}[-.\s]?\d{5}|\+\d{1,4}[-.\s]?\d+', phone_text):
                    # Clean the phone number
                    return ''.join(c for c in phone_text if c.isdigit() or c == '+')
        
        # Look for href attributes with tel: links
        tel_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'tel:')]")
        if tel_links:
            for link in tel_links:
                href = link.get_attribute("href")
                if href.startswith("tel:"):
                    return href.replace("tel:", "")
    
    except Exception as e:
        print(f"Error searching for phone number: {str(e)}")
    
    return "Phone Number Not Found"'''

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

        return {'URL': url, 'Name': name, 'Address': address, 'Website': website, 'Phone': phone}

    except WebDriverException as e:
        print(f"Error processing URL {url}: {str(e)}")
        return {
          
            'URL': url,
            'Address': 'Error',
            'Website': 'Error',
            'Phone': 'Error'
        }

def main():
    # Check if the input CSV file exists
    input_filename = 'stationery_shops_chennai_master.csv'
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
    output_filename = 'stationery_shops_chennai_master_output.csv'

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

    # Initialize the driver
    options = uc.ChromeOptions()
    # Optional: Add some Chrome options to improve scraping
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 15)  # Increased timeout

    # Counters for real-time progress tracking
    total_urls = len(urls)
    processed_new = 0
    skipped_existing = 0
    errors = 0

    print(f"\n{'='*80}")
    print(f"STARTING REAL-TIME INCREMENTAL DATA EXTRACTION")
    print(f"{'='*80}")
    print(f"Total URLs to process: {total_urls}")
    print(f"Output file: {output_filename}")
    print(f"Mode: Real-time incremental CSV writing")
    print("-" * 80)

    try:
        # Process each URL with real-time saving
        for index, url in enumerate(urls, 1):
            print(f"\n[{index}/{total_urls}] Processing URL: {url}")

            # Check if this URL was already processed (for resume capability)
            if check_url_already_processed(url, output_filename):
                print(f"⏭️  Skipping - already processed")
                skipped_existing += 1
                continue

            try:
                # Extract data from the URL
                result = scrape_data(url, driver, wait)

                # REAL-TIME SAVING: Immediately append to CSV
                write_header = (index == 1 and not file_exists and skipped_existing == 0)
                success = append_result_to_csv(result, output_filename, write_header)

                if success:
                    processed_new += 1
                    print(f"✅ Extracted and saved: {result.get('Name', 'N/A')}")
                    print(f"   Address: {result.get('Address', 'N/A')[:50]}...")
                    print(f"   Phone: {result.get('Phone', 'N/A')}")
                    print(f"   Progress: {processed_new} new + {skipped_existing} existing = {processed_new + skipped_existing}/{total_urls}")
                else:
                    errors += 1
                    print(f"❌ Failed to save result to CSV")

            except Exception as e:
                errors += 1
                print(f"❌ Error processing URL: {str(e)}")

                # Still try to save an error record
                error_result = {
                    'URL': url,
                    'Name': 'Error',
                    'Address': 'Error',
                    'Website': 'Error',
                    'Phone': 'Error'
                }
                write_header = (index == 1 and not file_exists and skipped_existing == 0)
                append_result_to_csv(error_result, output_filename, write_header)

            # Add delay between requests to avoid being blocked
            if index < total_urls:
                print(f"⏳ Waiting 2 seconds before next URL...")
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n⚠️  Script interrupted by user")
        print(f"✅ Progress saved: {processed_new} URLs processed and saved to {output_filename}")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print(f"✅ Progress saved: {processed_new} URLs processed and saved to {output_filename}")

    finally:
        # Close the driver safely
        safe_driver_quit(driver)

        # Final summary
        print(f"\n{'='*80}")
        print(f"EXTRACTION COMPLETED!")
        print(f"{'='*80}")
        print(f"Total URLs: {total_urls}")
        print(f"New URLs processed: {processed_new}")
        print(f"Already existing (skipped): {skipped_existing}")
        print(f"Errors encountered: {errors}")
        print(f"Output file: {output_filename}")

        # Count final records in output file
        try:
            if os.path.exists(output_filename):
                with open(output_filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    final_count = sum(1 for row in reader)
                print(f"Total records in output file: {final_count}")
            else:
                print(f"No output file created")
        except Exception as e:
            print(f"Warning: Could not count final records: {e}")

        print("="*80)

if __name__ == "__main__":
    main()
    
    
'''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import time
import csv
import pandas as pd
import re

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
                
                # Use regex to extract phone number (using raw string)
                phone_match = re.findall(r'\d{3,}[-\s]?\d{3,}[-\s]?\d{4}', phone_text)
                
                if phone_match:
                    # Return the first matched phone number
                    return phone_match[0].replace(' ', '').replace('-', '')
        
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
       
        address = "Not Found"
        website = "Not Found"
        phone = "Not Found"
        
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
            company_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))) 
            company = company_name.text
        except (TimeoutException, NoSuchElementException):
            pass

        # Phone number extraction
        phone = extract_phone_number(driver, wait)

        return {
            'Company Name': company,
            'URL': url,
            'Address': address,
            'Website': website,
            'Phone': phone
        }
    except WebDriverException as e:
        print(f"Error processing URL {url}: {str(e)}")
        return {
            'Company Name': "Not Found",
            'URL': url,
            'Address': 'Error',
            'Website': 'Error',
            'Phone': 'Error'
        }

def main():
    # Read URLs from CSV file
    try:
        df = pd.read_csv('Catering_in_Mumbai.csv')  # Replace with your CSV file name
        urls = df['URL'].tolist()  # Assuming 'URL' is the column name
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return

    # Initialize the driver
    options = uc.ChromeOptions()
    # Optional: Add some Chrome options to improve scraping
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 15)  # Increased timeout
    
    # List to store results
    results = []

    try:
        # Process each URL
        for url in urls:
            print(f"Processing URL: {url}")
            result = scrape_data(url, driver, wait)
            results.append(result)
            print(results)
            time.sleep(2)  # Add delay between requests
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the driver
        driver.quit()
        
        # Save results to CSV
        try:
            df_results = pd.DataFrame(results)
            df_results.to_csv('Catering_in_Mumbai_output.csv', index=False)
            print("Results saved to output.csv")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    main()  '''
    
