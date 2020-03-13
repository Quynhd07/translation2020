from flask import Flask, render_template, redirect, request, flash
# from translate import Translator 
from googletrans import Translator
import tweets
from jinja2 import StrictUndefined
import os 
import sources
from string import capwords

app = Flask(__name__)
app.secret_key = os.getenv('translation2020_key')
# app.secret_key = 'test'

# API_KEY = os.environ[]

@app.route('/')
def homepage():
    """displays list of most frequent tokens use can choose from"""
    tokens = tweets.get_frequent_tokens()
    return render_template('homepage.html', tokens = tokens)


@app.route('/<token>')
def display_key(token):
    """display headlines"""
    token = capwords(token)
    choice = request.args.get("language")

    if choice == None:
        choice = 'en'

    language = Translator()

    outlets = [sources.get_npr(token), sources.get_nytimes(token)]

    translated_headings = []
    translated_descriptions = []
    links = []
    
    for i in range(0, len(outlets)):

        for url, heading, description in zip(outlets[i]['urls'],outlets[i]['headings'], outlets[i]['descriptions']):
            translated_headings.append(language.translate(heading, dest = choice).text)
            translated_descriptions.append(language.translate(description, dest = choice).text)
            links.append(url)

    return render_template("base.html", articles_links=zip(links, translated_headings, translated_descriptions), token=token)





if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)