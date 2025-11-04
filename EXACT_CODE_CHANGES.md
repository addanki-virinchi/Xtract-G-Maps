# Exact Code Changes Made to Google_Maps.py

## File: Google_Maps.py
## Function: scroll_google_maps_single_search(search_term, pincode)
## Lines: 372-416

### BEFORE (Original URL-Based Approach)

```python
def scroll_google_maps_single_search(search_term, pincode):
    """
    Scrape Google Maps for a single search term and pincode combination
    """
    driver = None
    all_data = []

    try:
        driver = create_stable_driver()

        # Create search query with pincode
        search_query = f'"{search_term} {pincode}"'
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
```

### AFTER (New Interactive Search Approach)

```python
def scroll_google_maps_single_search(search_term, pincode):
    """
    Scrape Google Maps for a single search term and pincode combination
    Uses interactive search method instead of URL-based approach
    """
    driver = None
    all_data = []

    try:
        driver = create_stable_driver()

        # Create search query with pincode
        search_query = f"{search_term} {pincode}"

        print(f"Searching for: {search_query}")

        # Navigate to base Google Maps URL
        maps_url = "https://www.google.com/maps/"
        print(f"Opening Google Maps: {maps_url}")
        driver.get(maps_url)

        # Wait for page to load
        print("Loading Google Maps...")
        time.sleep(3)

        # Wait for search box to be present
        print("Waiting for search box to load...")
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        print("✓ Search box found")

        # Clear and enter search query
        print(f"Entering search query: {search_query}")
        search_box.clear()
        search_box.send_keys(search_query)
        time.sleep(1)

        # Click search button
        print("Clicking search button...")
        search_button = driver.find_element(By.ID, "searchbox-searchbutton")
        search_button.click()

        # Wait for results to load
        print("Waiting for search results to load...")
        time.sleep(5)
```

## Key Differences

| Aspect | Before | After |
|--------|--------|-------|
| **URL Construction** | Complex encoding with hardcoded coords | Simple base URL |
| **Search Method** | Direct URL navigation | Interactive search box |
| **Element Waiting** | Implicit (time.sleep) | Explicit (WebDriverWait) |
| **Initial Wait** | 8 seconds | 3 seconds |
| **Search Box** | Not explicitly handled | Located by ID and interacted with |
| **Search Button** | Not explicitly handled | Located by ID and clicked |
| **Error Handling** | Basic | WebDriverWait timeout exceptions |

## Imports Already Present

All required imports are already in the file:
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
```

## Rest of Function Unchanged

The rest of the function (lines 418-604) remains completely unchanged:
- First result clicking logic
- Results panel loading
- URL collection and scrolling
- Error handling and cleanup
- Return statements

## Backward Compatibility

✅ **No changes to:**
- Function signature
- Return values
- CSV output format
- Integration with other functions
- Error handling patterns
- Driver cleanup logic

## Testing the Changes

The modified function will:
1. Navigate to `https://www.google.com/maps/`
2. Wait for search box with ID `searchboxinput`
3. Enter the search query (e.g., "Stationery store 600001")
4. Click search button with ID `searchbox-searchbutton`
5. Wait for results to load
6. Continue with existing scrolling and URL collection logic

All existing functionality after line 416 remains unchanged.

