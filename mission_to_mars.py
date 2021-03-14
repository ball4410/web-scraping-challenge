#!/usr/bin/env python
# coding: utf-8

# In[39]:


# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[ ]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[ ]:


# Define database and collection
db = client.mars_db
collection = db.articles


# In[ ]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[ ]:


# Retrieve page with the requests module
response = requests.get(url)
# response.text


# In[ ]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')


# In[ ]:


# Retrieve the parent divs for first article
results = soup.find('div', class_="content_title")
news_title = results.text.strip()
news_title


# In[ ]:


# Retrieve the subheader divs for first article
result = soup.find('div', class_="image_and_description_container")
news_p = result.find('div', class_="rollover_description_inner").text.strip()
news_p


# In[ ]:


#Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

full_img_el = browser.find_by_tag('button')[1]
full_img_el.click()

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

try: 
    img_url_rel = soup.find('img', class_='fancybox-image')
    print(img_url_rel)
    
except AttributeError:
    print("Not Found")
    


# In[35]:


browser.quit()


# In[ ]:


ex = img_url_rel['src']
ex

full_img_url ='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + ex

full_img_url


# In[97]:


url = "https://space-facts.com/mars/"

tables = pd.read_html(requests.get(url).text)
tables

df = tables[0]

df.columns = ["Description", "Mars"]
df.set_index("Description", inplace = True)
df.head()


# In[98]:


html_table = df.to_html()
html_table

df.to_html('table.html')

get_ipython().system('open table.html')


# In[116]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
    sample_link = browser.links.find_by_text("Sample").first
    img_url = sample_link["href"]
    
    hemispheres['title'] = link
    hemispheres['img_url'] = img_url
    
    hemisphere_and_images_urls.append(hemispheres)
        
    browser.back()


# In[112]:


browser.quit()


# In[117]:


hemisphere_and_images_urls


# In[ ]:




