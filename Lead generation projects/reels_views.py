import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up the Chrome driver
service = Service()

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_argument("--incognito")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Instagram base URL
url = "https://www.instagram.com/"
reels_data = []  # Initialize the list to store reel URLs and view counts

try:
    driver.get(url)
    time.sleep(5)

    # Add the sessionid cookie (replace with your sessionid value)
    cookie = {'name': 'sessionid',
              'value': "cookie value",
              'domain': '.instagram.com'}
    driver.add_cookie(cookie)

    # Refresh the page to apply the session cookie and ensure you are logged in
    driver.refresh()
    time.sleep(5)

    # Navigate to the specific Instagram account's reels page
    reels_url = "https://www.instagram.com/sankeshsurana/reels/"
    driver.get(reels_url)
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Find all reels on the current page
        reels = driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')

        for reel in reels:
            reel_url = reel.get_attribute("href")

            try:
                # Extract the view count for each reel
                view_count_element = reel.find_element(By.XPATH, './/div[2]/div[2]/div/div/div/span')
                view_count = view_count_element.text
            except NoSuchElementException:
                view_count = "N/A"  # Handle case where view count is not found

            reels_data.append((reel_url, view_count))
            print(f"Reel URL: {reel_url} | Views: {view_count}")

        # Scroll down to load more reels
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Calculate the new scroll height and compare it to the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Break the loop if no new content is loaded
        if new_height == last_height:
            break
        last_height = new_height

# Catching any general exceptions so we can still save the data
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Save the results to a CSV file
    try:
        with open('reels_view_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Reel URL', 'View Count'])
            # Write the data
            writer.writerows(reels_data)
        print("Data saved to reels_view_data.csv successfully.")
    except Exception as e:
        print(f"Failed to write to CSV: {e}")

    # Quit the WebDriver after completion
    try:
        driver.quit()
    except WebDriverException as e:
        print(f"Error closing the WebDriver: {e}")

# Print the total scraped data (optional)
print("Total reels scraped:", len(reels_data))
for reel_url, view_count in reels_data:
    print(f"Reel URL: {reel_url} | Views: {view_count}")

