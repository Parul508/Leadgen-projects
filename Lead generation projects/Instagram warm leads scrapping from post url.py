#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the Chrome driver
driver = webdriver.Chrome()

# Instagram URL
url = "https://www.instagram.com/"

# Open Instagram
driver.get(url)
time.sleep(2)

# Add the sessionid cookie (replace with your sessionid value)
cookie = {
    'name': 'sessionid',
    'value': '69448668266%3AfUdEpUZ7v2raiR%3A4%3AAYc3Zx9FTzDPmLzD7kwnU2l9-OknVmY1ZO3oJ4htfA',
    'domain': '.instagram.com'
}
driver.add_cookie(cookie)

# Refresh to apply the cookie and log in
driver.refresh()
time.sleep(5)

# Navigate to the post URL
post_url = "https://www.instagram.com/p/DByLH5MR5jE/?img_index=1"
driver.get(post_url)
time.sleep(4)

# Initialize empty lists for usernames and comments
user_names = []
user_comments = []

# Scroll to load comments dynamically
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0

while scroll_attempts < 5:  # Adjust this limit as needed
    try:
        # Extract comments
        comments = driver.find_elements(By.CSS_SELECTOR, "ul li")  # More general selector for list items
        for c in comments:
            try:
                # Look for username and comment text
                name = c.find_element(By.CSS_SELECTOR, "h3 a").text  # Update with actual tag structure
                content = c.find_element(By.CSS_SELECTOR, "span").text
                content = content.replace('\n', ' ').strip().rstrip()
                if name not in user_names or content not in user_comments:
                    user_names.append(name)
                    user_comments.append(content)
            except Exception as e:
                print(f"Error extracting a comment: {e}")

        # Scroll down to load more comments
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # Allow time for comments to load

        # Check if new content has loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1  # Increment if no new content is loaded
        else:
            scroll_attempts = 0  # Reset attempts if new content is loaded
        last_height = new_height

    except Exception as e:
        print(f"Error while scrolling: {e}")
        break

# Combine the usernames and comments into a DataFrame
if user_names and user_comments:
    data = pd.DataFrame({'Username': user_names, 'Comment': user_comments})
    # Export to an Excel file
    data.to_excel('instagram_comments.xlsx', index=False)
    print("Comments successfully saved to 'instagram_comments.xlsx'")
else:
    print("No comments found or extracted.")

# Close the driver
driver.quit()


# In[ ]:




