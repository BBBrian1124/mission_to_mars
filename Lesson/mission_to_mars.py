#!/usr/bin/env python
# coding: utf-8

# # We want to parse the site to obtain information on the newest article
# # Import Dependencies and Setup

# In[1]:
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import Pandas
import pandas as pd


# In[2]:


# Setup the browser as chrome to run our web scrape 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# # Web Scrape

# ### Mars Articles

# In[3]:


# Define and visit the webpage url
url = 'https://redplanetscience.com'
browser.visit(url)
# search for elements with the specific combination of <div /> tag and list_text attribute 
# Optional 1 second delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Parse thorugh the html on the webpage 
html = browser.html
news_soup = soup(html, 'html.parser')
# the . tells us to look at that class, so this searches the <div /> tag and list_text attribute
# css usually looks left to right, so it will find the last value, that is why we use 'select_one' to get the first element
slide_elem = news_soup.select_one('div.list_text')

# When inspecting the webpage the below is the html code
slide_elem


# In[5]:


# Find the title which we see is in the <div /> tag and 'content_title' class
slide_elem.find('div', class_='content_title')


# In[6]:


# Use .get_text() to parse just the text from the above code 
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Find the article body by doing .find on that tag and class then get just the text 
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Define and visit the url
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# On that browser it opens up a webpage where we want the first image 
# There is a button to click to enlarge/get the full image which we want our code to press automatically 
# If we inspect the html code for the button the code is: <button class="btn btn-outline-light"> FULL IMAGE</button> 
# Doing a search on the rest of the html we see there are 2 other <button /> tags

# We willl find the element by the tag 'button' and place it in a variable
# We know there are 2 other instances of the <button /> tag and know that the button we want is the 2nd one so we call that index
full_image_elem = browser.find_by_tag('button')[1]
# Then tell the code to click the button/variable
full_image_elem.click()


# In[10]:


# Now that we have opened the enlarged image, we need to parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
#img_soup

# The html code for the enlarged image is: <img class="fancybox-image" src="image/featured/mars1.jpg" alt="">


# In[11]:


# We will use .find to look at the img tag and the class, then get just the src value
# We want to get the src value rather than the value itself because the value will update 
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Now that we have the most recent web image location we can use a string concatination to add it to the base url 
# This will allow us to generate a link to the most recent image even if it updates 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
print(img_url)


# ### Mars Facts

# In[13]:


# The information we want is in a table on the webpage which is formatted as so
# We can see that it's already in a table format with the table being the class 
    # followed by the body
        # followed by each row of the table
            # which contains a columnn for the header 
            # and a column for the data/values

# <table class="table table-striped">
# 				  <tbody>
# 				    <tr>
# 				      <th scope="row">Equatorial Diameter:</th>
# 				      <td>6,792 km</td>
# 				    </tr>
# 				    <tr>
# 				      <th scope="row">Polar Diameter:</th>
# 				      <td>6,752 km</td>
# 				    </tr>
# 				  </tbody>
# 				</table>


# In[14]:


# We can use Panda's built in function .read_html to read tables from html, and we specify index as 0 to get the first table
# Pandas then stores it into a DataFrame 
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Specify the column headers for the DataFrame
df.columns=['description', 'Mars', 'Earth']
# Set the index for the for the DataFrame
# inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable
df.set_index('description', inplace=True)
df


# In[15]:


# Because we want to update/pass this DataFrame to our own webpage, we need to convert it back to html format 
df.to_html()


# In[16]:


# Quit the automated browser session
browser.quit()

