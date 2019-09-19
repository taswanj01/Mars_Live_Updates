import pandas as pd
from splinter import Browser
import time


def init_browser():
    # function to initialize browser and define path to chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def mars_scrape():
    
    browser = init_browser()
    mars_data = {}

    #  Latest News on Mars from NASA
    #-------------------------------------------------------
    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    # Send Splinter to Mars news page and give page time to load
    browser.visit(mars_news_url)
    time.sleep(5)

    # Navigate Splinter to the news articles section, find and store the first articles title and paragraph text
    mars_latest_news_title_first_li = browser.find_by_css('body .item_list .slide').first
    mars_data["Mars_latest_news_title"] = mars_latest_news_title_first_li.find_by_css('.content_title a').value
    mars_data["Mars_latest_news_text"] = mars_latest_news_title_first_li.find_by_css('.article_teaser_body').value
    #####################################################


    #  Current feaured image
    #-------------------------------------------------------
    # Collect the current 'featured' Mars image from JPL site
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit'
    browser.visit(mars_image_url)
    time.sleep(5)

    #Navigate first click to get to full res image
    browser.find_by_id('full_image').first.click()
    time.sleep(5)

    # Next click to get further to full res image
    browser.click_link_by_text('more info     ')
    time.sleep(5)

    # Save the URL of the image
    mars_data["Mars_latest_featured_image"] = browser.find_by_css('figure.lede a')['href']
    ######################################################


    #  Weather on Mars
    #-------------------------------------------------------
    mars_weather_twitter_url = 'https://twitter.com/MarsWxReport/media?lang=en'
    browser.visit(mars_weather_twitter_url)
    time.sleep(5)
    
    # Save the latest tweet giving the weather
    mars_data["Mars_weather"] = browser.find_by_css('.TweetTextSize.TweetTextSize--normal.js-tweet-text.tweet-text').first.text
    ######################################################


    #  Mars facts
    #------------------------------------------------------- 
    # General facts about the planet including Diameter, Mass, etc. in table form
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_raw_html = pd.read_html(mars_facts_url)
    mars_html = mars_raw_html[0]
    mars_html.rename(columns={0:"description", 1:"value"}, inplace=True)
    mars_html.set_index("description", inplace=True)
    mars_data["Mars_facts_table"] = mars_html.to_html()
    ######################################################

    #  High res images of the 4 Mars hemispheres
    #-------------------------------------------------------
    # Url for hemisphere images, visit main page for hemishperes
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(5)

    # List to hold dictionaries of each images title and full size pic URL
    hemisphere_image_urls = []
    
    # Four hemispheres so we can hard code the range
    # Iterate through the four pages and collect title and URL, sleeps are to allow browser time parse page
    for link in range(4):
        hemis_links = browser.find_by_css('.results .item')
        hemis_links[link].find_by_css('a img').click()
        time.sleep(3)
        hemi_title = browser.find_by_css('section.block.metadata h2').value
        hemisphere_image_urls.append({'title':hemi_title.strip('Enhanced'), 'img_url': browser.find_by_css('.downloads ul li a')['href']})
        browser.back()
        time.sleep(3)
    
    mars_data["Mars_hemispheres_pics"] = hemisphere_image_urls
    ######################################################

    browser.quit()
    
    return mars_data 