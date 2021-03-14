#!/usr/bin/env python
# coding: utf-8
# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        news_title, news_paragraph = mars_news(browser)
        
        data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" :hemispheres(browser)
        }       
        browser.quit()
        return data

    
def mars_news(browser):
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # Retrieve page with the requests module
    response = requests.get(url)
    # response.text


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Retrieve the parent divs for first article
        results = soup.find('div', class_="content_title")
        news_title = results.text.strip()
        print(news_title)


        # Retrieve the subheader divs for first article
        result = soup.find('div', class_="image_and_description_container")
        news_p = result.find('div', class_="rollover_description_inner").text.strip()
        print(news_p)
        
    except: 
        return None, None
    
    return news_title, news_p
    
def featured_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    full_img_el = browser.find_by_tag('button')[1]
    full_img_el.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try: 
        img_url_rel = soup.find('a', class_='showing fancybox-thumbs')

    except AttributeError:
        return None
    
    full_img_url =f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/mars1.jpg'

    return full_img_url 

def mars_facts():

    df = pd.read_html("https://space-facts.com/mars/")[0]

    df.columns = ["Description", "Mars"]
    df.set_index("Description", inplace = True)

    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('h3')
    hemisphere_and_images_urls = []

    for x in links:

        hemispheres = {}

        link = x.text
        browser.links.find_by_partial_text(x.text).click()
        
        try:
            sample_link = browser.links.find_by_text("Sample").first
            img_url = sample_link["href"]

            hemispheres['title'] = link
            hemispheres['img_url'] = img_url

            hemisphere_and_images_urls.append(hemispheres)
            browser.back()
        except:
            return None  

    return hemisphere_and_images_urls



