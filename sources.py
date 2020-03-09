
from requests import get
from bs4 import BeautifulSoup, re, Comment
import string 
from datetime import date

# create list of keywords 
key_words = string.capwords('election')


def get_npr():
    url = "https://www.npr.org/sections/politics/"
    response = get(url)
    response_html = BeautifulSoup(response.text, "html.parser")
    # find headings that contains the key_words; limit search results to 3
    # find_all returns a list of tag objects
    article_containers = response_html.find_all("div", class_= "item-info")
    
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
        # remove date from <p>
        format_description = matched_articles[i].find('p').text[16:]
        article_dict['descriptions'].append(format_description)
        article_dict['urls'].append(matched_articles[i].find('h2').find('a')['href'])

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

    






