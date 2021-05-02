#!/usr/bin/env python
# coding: utf-8

# # We want to parse the site to obtain information on the newest article

# Import Dependencies and Setup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# # Web Scrape

# Scrape all
def scrape_all():
    # Setup the browser as chrome to run our web scrape 
    executable_path = {'executable_path': 'chromedriver.exe'}
    # We will change headless to true since we no longer need to see the window open as it did if it were false
    browser = Browser('chrome', **executable_path, headless=True)
    # we're going to set our news title and paragraph variables (remember, this function will return two values).
    # This line of code tells Python that we'll be using our mars_news function to pull this data.
    news_title, news_paragraph = mars_articles(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        # Runs our featured_image function and stores in the dictionary
        "featured_image": featured_image(browser),
        # Runs our mars_facts function and stores it in the dictionary
        "facts": mars_facts(),
        # Runs the time this is run to see the last modified date 
        "last_modified": dt.datetime.now()
    }
  # Stop webdriver and return data
    browser.quit()
    return data


# ### Mars Articles

# Refactor our code for parsing the mars articles
    # create a function for it to return the news_title and news_p instead of printing like we did in jupyter
    # pass a required variable to the function which we've defined outside of this function
def mars_articles(browser):
    # Define and visit the webpage url
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # search for elements with the specific combination of <div /> tag and list_text attribute 
    # Optional 1 second delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse thorugh the html on the webpage 
    html = browser.html
    news_soup = soup(html, 'html.parser')

     # Add try/except for error handling 
        # Most common is if the webpage format changes and the code no longer matches 
        # this will return an AttributeError 
    try:
        # the . tells us to look at that class, so this searches the <div /> tag and list_text attribute
        # css usually looks left to right, so it will find the last value, that is why we use 'select_one' to get the first element
        slide_elem = news_soup.select_one('div.list_text')

        # When inspecting the webpage the below is the html code
        slide_elem

        # Find the title which we see is in the <div /> tag and 'content_title' class
        slide_elem.find('div', class_='content_title')

        # Use .get_text() to parse just the text from the above code 
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Find the article body by doing .find on that tag and class then get just the text 
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p

    # If an error is found, the code will return nothing and continue the rest of the code
    except AttributeError:
        return None, None

    # Instead of printing these values we will return them         
    return news_title, news_p

# ### Featured Images
# Similarily we will create a function for the featured_image to take our pre-defined browser variable
def featured_image(browser):
    # Define and visit the url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # On that browser it opens up a webpage where we want the first image 
    # There is a button to click to enlarge/get the full image which we want our code to press automatically 
    # If we inspect the html code for the button the code is: <button class="btn btn-outline-light"> FULL IMAGE</button> 
    # Doing a search on the rest of the html we see there are 2 other <button /> tags

    # We will find the element by the tag 'button' and place it in a variable
    # We know there are 2 other instances of the <button /> tag and know that the button we want is the 2nd one so we call that index
    full_image_elem = browser.find_by_tag('button')[1]
    # Then tell the code to click the button/variable
    full_image_elem.click()

    # Now that we have opened the enlarged image, we need to parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #img_soup
    # The html code for the enlarged image is: <img class="fancybox-image" src="image/featured/mars1.jpg" alt="">

    # Add try/except for error handling
    try:

        # We will use .find to look at the img tag and the class, then get just the src value
        # We want to get the src value rather than the value itself because the value will update 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    
    # If there is an error it will return nothing and continue the rest of the code 
    except AttributeError:
        return None
    
        # Now that we have the most recent web image location we can use a string concatination to add it to the base url 
        # This will allow us to generate a link to the most recent image even if it updates 
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #print(img_url)

    # Remove any code that would print out values and return them instead 
    return img_url 

# ### Mars Facts
def mars_facts():
    
    try:
        # We can use Panda's built in function .read_html to read tables from html, and we specify index as 0 to get the first table
        # Pandas then stores it into a DataFrame 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    # A BaseException is a little bit of a catchall when it comes to error handling. 
    # It is raised wh   en any of the built-in exceptions are encountered
        # it won't handle any user-defined exceptions
        # we need to use is since we are using read_html to pull data so it can return different errors
    except BaseException:
      return None

    # Specify the column headers for the DataFrame
    df.columns=['description', 'Mars', 'Earth']
    # Set the index for the for the DataFrame
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable
    df.set_index('description', inplace=True)
    #df

    # Because we want to update/pass this DataFrame to our own webpage, we need to convert it back to html format 
    #df.to_html()
    # Remove the code that prints and replace it with return 
    return df.to_html()

# This last block of code tells Flask that our script is complete and ready for action
# The print statement will print out the results of our scraping to our terminal after executing the code
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())