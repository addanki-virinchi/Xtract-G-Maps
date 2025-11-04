
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# --- User Inputs ---
search_term = "Stationery store"
pincode = "600021"

# --- Combine Search Query ---
search_query = f"{search_term} {pincode}"
encoded_query = search_query.replace(" ", "+")
maps_url = f"https://www.google.com/maps/"

# --- Set up Selenium --
driver = uc.Chrome()
options = uc.ChromeOptions()
options.add_argument("--start-maximized")


try:
    # --- Open Google Maps ---
    driver.get(maps_url)
    print(f"Opening Google Maps for: {search_query}")

    # --- Wait for Search Box ---
    wait = WebDriverWait(driver, 15)
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))

    # --- Clear and Type Query ---
    search_box.clear()
    search_box.send_keys(f"'{search_query}'")

    time.sleep(1)

    # --- Click Search Button ---
    search_button = driver.find_element(By.ID, "searchbox-searchbutton")
    search_button.click()

    print(f"Searching for: {search_query}")
    time.sleep(5)

finally:
    # Optionally keep browser open or close
    driver.quit()
