from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # --- Visit Mars News site ---
    # Setting url
    url = 'https://mars.nasa.gov/news/'
    
    # Visit url with splinter
    browser.visit(url)

    time.sleep(1)

    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Extracting the latest news and paragraph texts
    title_results = soup.find_all('div', class_='content_title')
    
    par_results = soup.find_all('div', class_='article_teaser_body')

    news_title = title_results[1].text
    
    news_p = par_results[0].text


    # Setting the url# Setting the url
    
    # Setting URL for Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Visit URL with splinter
    browser.visit(url)

    # Find the id"full_image"
    find_id = browser.find_by_id('full_image')
    
    # Click on the text
    find_id.click()
    
    # Find "more info" and set up a wait time
    browser.is_element_not_present_by_text('more info', wait_time=1)
    
    # Click on "more info"
    more_info = browser.click_link_by_partial_text('more info')
    
    # Parse HTML with Beautiful Soup
    soup = bs(browser.html, 'html.parser')
    
    # Extract the image link 
    results = soup.find('figure', class_='lede')
    img_path = results.a['href']
    
    # Concatenate the url with the relative image link 
    featured_image_url = 'https://www.jpl.nasa.gov' + img_path

    # --- Mars Facts ---
    
    # Use pandas to extract the tables in the html
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    # Creating a dataframe with the tables
    df = tables[0]
    df.columns = ['Description', 'Value']
    
    # Converting to HTML table string
    html_table = df.to_html()
    html_table

    # --- Mars Hemispheres ---
   
    # Setting the url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Visit the url using splinter
    browser.visit(url)

    time.sleep(1)

    # Parse HTML with Beautiful Soup
    soup = bs(browser.html, 'html.parser')

    # Find all the items
    find_items = soup.find_all('div', class_='item')
    
    # Create a list for all the titles and image urls to live
    hemisphere_image_urls = []

    # Default url
    default_url = 'https://astrogeology.usgs.gov'
    
    # Loop through all the items and extract the titles
    for i in find_items: 
        
        title = i.find('h3').text
        
        specific_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link for the image
        browser.visit(default_url + specific_url)

         # Parse HTML with Beautiful Soup again
        soup = bs(browser.html, 'html.parser')

        # Extract the image link links
        img_url = default_url + soup.find('img', class_='wide-image')['src']
        
        # Append the title and img_url to the list
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})    

    hemisphere_image_urls

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data