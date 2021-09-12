# Import Dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'http://redplanetscience.com'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    latestTitle=soup.find_all('div',class_="content_title")[0].text
    latestTeaser=soup.find_all('div',class_="article_teaser_body")[0].text

    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    partial_url = soup.find('a',class_='showimg fancybox-thumbs')['href']
    featured_image_url=url +'/'+partial_url
    browser.quit()

    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)[1]
    table.rename(columns={0:'Fact',1:'Value'},inplace=True)

    html_table= table.to_html()
    html_table=html_table.replace('\n', '')
    html_table

    url = 'https://marshemispheres.com/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    results = soup.find_all('div', class_='description')

    hemisphere_image_urls=[]
    for each in results:
        title = each.h3.text    
        response = requests.get(f'https://marshemispheres.com/{each.a["href"]}')
        soup = bs(response.text,'lxml')
        hemiResult=soup.find_all('dd')[1].a['href']
        hemisphere_image_urls.append({
            "title":title[0:-9],
            "img_url":f'https://marshemispheres.com/{hemiResult}'
            })
    mars_data = {
        'latestTitle':latestTitle,
        'latestTeaser':latestTeaser,
        'featuredImage':featured_image_url,
        'htmlTable':html_table,
        'hemishpereDict':hemisphere_image_urls
    }
    
    return mars_data
