#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# We will use splinter to click on links
# https://splinter.readthedocs.io/en/latest/elements-in-the-page.html

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# First find where the image URLs are using Splinter
# Inspect the html of the web page and we can see that they are stored in the product title
    # which is under the <a /> tag and product-item 
    # the title itself is stored in h3
imgs_links= browser.find_by_css("a.product-item h3")

# We know there are 4 results so create a loop to loop through 4 times
for x in range(0,4):
    
    # Create an empty list
    hemisphere={}
    
    # Click on the header/title to open the link using Splinter 
    # This link has the enlarged image which we want 
    browser.find_by_css("a.product-item h3")[x].click()
    
    # The enlarged image is stored under the "Sample" text/link 
    # Find the first instance of sample
    enlarged_img= browser.links.find_by_text("Sample").first
    # Place the enlarged image into the list under img_url
    hemisphere['img_url']=enlarged_img['href']
    
    # On the newly opened webpage, the title is stored under h2 in the title class
    # Extract the text from that section
    hemisphere['title']=browser.find_by_css("h2.title").text
    
    # Add Objects to hemisphere_image_urls list
    hemisphere_image_urls.append(hemisphere)
    
    #Go Back
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()


# In[ ]:




