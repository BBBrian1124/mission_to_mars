# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Call our mars_article function
    news_title, news_paragraph = mars_articles(browser)

  # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        # Runs our featured_image function and stores in the dictionary
        "featured_image": featured_image(browser),
        # Runs our mars_facts function and stores it in the dictionary
        "facts": mars_facts(),
        # Obtain the hemisphere data
        "hemispheres": hemispheres(browser),
        # Runs the time this is run to see the last modified date 
        "last_modified": dt.datetime.now()
    }
 # Stop webdriver and return data
    browser.quit()
    return data

# Mars Articles 
def mars_articles(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # First try to find the first element of the div.list_test and find the 'title' in the div tag and class
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Except when there is an attribute error or no result, return nothing
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # If attribute error/no results found, return none    
    except AttributeError:
        return None
   
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Mars Facts
def mars_facts():
    try: 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None 
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html()


def hemispheres(browser):
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # ### Hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

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
        hemispheres={}
            
        # Click on the header/title to open the link using Splinter 
        # This link has the enlarged image which we want 
        browser.find_by_css("a.product-item h3")[x].click()
            
        # The enlarged image is stored under the "Sample" text/link 
        # Find the first instance of sample
        enlarged_img= browser.links.find_by_text("Sample").first
        # Place the enlarged image into the list under img_url
        hemispheres['img_url']=enlarged_img['href']
            
        # On the newly opened webpage, the title is stored under h2 in the title class
        # Extract the text from that section
        hemispheres['title']=browser.find_by_css("h2.title").text
            
        # Add Objects to hemisphere_image_urls list
        hemisphere_image_urls.append(hemispheres)
            
        #Go Back
        browser.back()
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())