#!/usr/bin/env python
# coding: utf-8

# In[2]:


# cold leadgen from instagram by using session id or by using hashtag.

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  
import time as t
from bs4 import BeautifulSoup  
import pandas as pd  

# Set up Chrome options for incognito
chrome_options = Options()
chrome_options.add_argument("--incognito")

# Set up the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)

# Instagram URL
url = "https://www.instagram.com/"

# Open Instagram
driver.get(url)
t.sleep(2)

# Add sessionid cookie (replace with your sessionid value)
cookie = {'name': 'sessionid', 'value': '#paste your session ID here'}
driver.add_cookie(cookie)

# Refresh to apply the cookie and log in
driver.refresh()
t.sleep(5)

# Function to search for posts using a hashtag
def search_hashtag_and_profiles(hashtag):
    hashtag_url = f'https://www.instagram.com/explore/tags/{hashtag}/'  # hashtag URL format
    driver.get(hashtag_url)
    t.sleep(5)
    
    scroll_count = 5  # Number of times to scroll for more results
    extracted_posts = []
    profiles_with_posts = []  # Initialize the list correctly here
    
    for _ in range(scroll_count):
        # Parse the current page source with BeautifulSoup
        page_source = driver.page_source  # Get the page source first
        soup = BeautifulSoup(page_source, 'html.parser')  # Initialize BeautifulSoup
        
        # Find all posts and their links on the hashtag page
        posts = soup.find_all('a', href=True)
        
        for post in posts:
            post_link = post['href']
            
            # Filter for relevant posts and links (only Instagram posts start with /p/)
            if post_link.startswith('/p/'):
                full_link = f'https://www.instagram.com{post_link}'
                if full_link not in extracted_posts:
                    extracted_posts.append(full_link)
                    print(f'Post Link: {full_link}')
                    
                    # Visit the post page to extract the profile information
                    driver.get(full_link)
                    t.sleep(3)  # Wait for the page to load
                    
                    # Parse the post page
                    post_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Find the username (usually inside an <a> tag with a href pointing to the profile)
                    profile_tag = post_page_soup.find('a', href=True)
                    
                    if profile_tag:
                        username = profile_tag.text.strip()  # Extract the username
                        profile_link = f"https://www.instagram.com{profile_tag['href']}"  # Profile link
                        
                        # Save username and post link
                        profiles_with_posts.append({'username': username, 'profile_link': profile_link})
                        print(f"Username: {username}, Profile Link: {profile_link}")
        
        # Scroll down to load more results on the hashtag page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        t.sleep(3)

    return profiles_with_posts

# Search for any hashtag
hashtag = '#paste your hashtag here'  # Specify the hashtag without '#'
search_hashtag_and_profiles(hashtag)

# Close the browser after task completion
print("completed")
driver.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




