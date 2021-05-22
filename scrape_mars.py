from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #start up browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #NASA Mars News
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    #start up parser
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #scrape the first headline and paragraph 
    NASA_title = soup.find("div", class_="content_title").get_text() 
    NASA_par = soup.find("div", class_="article_teaser_body").get_text() 

    #JPL Mars Space Images - Featured Image
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)
    #start up parser
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #pull the featured image
    featured_image = soup.find("img", class_="headerimage fade-in")['src']
    featured_image_url = url2 + featured_image

    #Mars Facts - Table
    url3 = "https://galaxyfacts-mars.com/"
    mars_tables = pd.read_html(url3)
    #only want the table on Mars
    mars_table = mars_tables[1]
    mars_table = mars_table.rename(columns = {0:"Fact", 1:"Data"})
    html_mars_table = mars_table.to_html()

    #Mars Hemispheres
    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    #start up parser
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #starting lists/dictonaries
    hem_titles = []
    hem_urls = []
    #pulling hemisphere names
    for hem_title in soup.findAll("h3"):
        hem_titles.append(hem_title.get_text())
    #removing back from list
    hem_titles.pop()

    #running through hemisphere pages to grab pictures 
    for hem_title in hem_titles:
        browser.links.find_by_partial_text(hem_title).click()
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        base_hem_url = soup.find("img", class_="wide-image")['src']
        hem_url = url4 + base_hem_url
        hem_urls.append(hem_url)
        #going back to the main page to grab the next one
        browser.links.find_by_partial_text('Back').click()

    #moving lists into dictonary and then adding labels by processing it through a dataframe
    base_dict = dict(zip(hem_titles, hem_urls))
    hem_dict = pd.DataFrame(list(base_dict.items()),columns=["title", "img_url"])
    hemisphere_image_urls = hem_dict.to_dict('records')

    #finish scraping 
    browser.quit()
    
    #saving data to db
    mars = {
        'NASA_title' : NASA_title,
        'NASA_par' : NASA_par,
        'featured_image' : featured_image_url,
        'mars_table' : html_mars_table,
        'hem_data' : hemisphere_image_urls
    }
    return mars