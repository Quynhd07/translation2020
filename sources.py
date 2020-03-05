
from requests import get
from bs4 import BeautifulSoup



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
    article_containers = response_html.find_all("div", class_ ='item-info-wrap')
    headings = []
    for i in range(0,3):
        headings.append(article_containers[i].text)

    return headings

