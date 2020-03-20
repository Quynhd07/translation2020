
from requests import get
from bs4 import BeautifulSoup, re, Comment
from datetime import date


def get_npr(token) -> dict:
    """returns dict of headlines from NPR that match keyword"""
    url = "https://www.npr.org/sections/politics/"
    # request and store the page's response as response variable 
    response = get(url)
    # create beautifulsoup object and parse through page 
    response_html = BeautifulSoup(response.text, "html.parser")
    # find_all returns a list of tag objects
    article_containers = response_html.find_all("div", class_= "item-info")
    
    matched_articles = []
    # find headings that contains the token; add to matched_articles list 
    for article in article_containers:
        if token in article.find("h2").text:
            matched_articles.append(article)

    # create dict to store info from each article 
    article_dict = {
        'headings': [],
        'descriptions': [],
        'urls': []
        # 'date': date.today().isoformat()
    }
   
    # iterate through matched_articles to populate article_dict
    for i in range(0,len(matched_articles)):
        article_dict['headings'].append(matched_articles[i].find('h2').text)
        # remove date from <p>
        format_description = matched_articles[i].find('p').text[16:]
        article_dict['descriptions'].append(format_description)
        article_dict['urls'].append(matched_articles[i].find('h2').find('a')['href'])

    # return article_dict
    return article_dict


def get_nytimes(token) -> dict:
    """returns dict of headlines from NPR that match keyword"""
    url = "https://www.nytimes.com/section/politics"
    response = get(url)
    response_html = BeautifulSoup(response.text, "html.parser")
    article_containers = response_html.find_all("div", class_ = "css-1l4spti")

    matched_articles = []

    for article in article_containers:
        if token in article.find("h2").text:
            matched_articles.append(article)


    article_dict = {
        'headings': [],
        'descriptions': [],
        'urls': [],
        'date': date.today().isoformat()
    }
   
    for i in range(0,len(matched_articles)):
        article_dict['headings'].append(matched_articles[i].find('h2').text)
        article_dict['descriptions'].append(matched_articles[i].find('p').text)
        full_url = 'https://www.nytimes.com' + matched_articles[i].find('a')['href']
        article_dict['urls'].append(full_url)
        
    return article_dict


def get_sources(token) -> list:
    """combines all sources into one list"""
    combined_sources = []
    sources_list = [get_npr, get_nytimes]
    for source in sources_list: 
        combined_sources.append(source(token))

    return combined_sources 

