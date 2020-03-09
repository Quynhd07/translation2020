from flask import Flask, render_template, redirect, request, flash

from translate import Translator 

# from jinja2 import StrictUndefined


import os 

import sources

app = Flask(__name__)
app.secret_key = os.getenv('translation2020_key')
# app.secret_key = 'test'

# API_KEY = os.environ[]

@app.route('/')
def homepage():
    """display headlines"""

    choice = request.args.get("language")
    
    if choice == None:
        choice = 'en'

    language = Translator(to_lang=choice)


    outlets = [sources.get_npr(), sources.get_nytimes()]

    translated_headings = []
    translated_descriptions = []
    links = []
    
    for i in range(0, len(outlets)):

        for url, heading, description in zip(outlets[i]['urls'],outlets[i]['headings'], outlets[i]['descriptions']):
            translated_headings.append(language.translate(heading))
            translated_descriptions.append(language.translate(description))
            links.append(url)

    return render_template("base.html", articles_links = zip(links, translated_headings, translated_descriptions))



if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)