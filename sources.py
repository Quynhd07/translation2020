
from requests import get
from bs4 import BeautifulSoup, re, Comment
import string 
from datetime import date

# create list of keywords 
key_words = string.capwords('trump')

def get_apnews():
    url = "https://apnews.com/apf-politics"
    # request the server content of apnews by using get()
    # store the page's response in ap_news variable response 
    response = get(url)

    # create beautifulsoup object
    # ap_news is now a response obj -> access its .text attribute 
    # "html.parser" indicates that we want to parse using Python's built-in html parser
    response_html = BeautifulSoup(response.text, "html.parser")
    article_containers = response_html.find_all("h1", class_ ='Component-h1-0-2-63')
    #return first 3 articles
    headings = []
    for i in range(0,3):
        headings.append(article_containers[i].text)

    return headings


def get_npr():
    url = "https://www.npr.org/sections/politics/"
    response = get(url)
    response_html = BeautifulSoup(response.text, "html.parser")
    # find headings that contains the key_words; limit search results to 3
    # find_all returns a list of tag objects
    article_containers = response_html.find_all("h2", string=re.compile(key_words), attrs = {'class':'title'}, limit = 3)
    # create dict with urls and headings


    article_dict = {
        'headings': [],
        'urls': [],
        'date': date.today().isoformat()
    }
   
    for i in range(0,len(article_containers)):
        article_dict['headings'].append(article_containers[i].text)
        article_dict['urls'].append(article_containers[i].find('a')['href'])

    # return article_dict
    return article_dict 


def get_nytimes():
    url = "https://www.nytimes.com/section/politics"
    response = get(url)
    response_html = BeautifulSoup(response.text, "html.parser")
    # find headings that contains the key_words; limit search results to 3
    article_containers = response_html.find_all("div", class_ = "css-1l4spti")
    # article_containers = response_html.find_all(string=lambda key_words: isinstance(key_words, Comment))
    # create dict with urls and headings

    matched_articles = []

    for article in article_containers:
        if key_words in article.find("h2").text:
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
        

    # return article_dict
    return article_dict

    






