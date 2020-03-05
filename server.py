from flask import Flask, render_template, redirect, request, flash

from translate import Translator 

# from jinja2 import StrictUndefined

# from requests import get 

import os 

import sources

app = Flask(__name__)
app.secret_key = os.getenv('translation2020_key')
print(os.getenv('translation2020_key'))
# app.secret_key = 'test'

# API_KEY = os.environ[]

@app.route('/')
def homepage():
    """display headlines"""

    vietnamese = Translator(to_lang="vi")

    outlets = [sources.get_apnews, sources.get_npr]
    names = ['APNEWS', 'NPR']

    vi_translation = []
    
    for i in range(0, len(outlets)):
        vi_translation.append(names[i])
        for heading in outlets[i]():
            translate_heading = vietnamese.translate(heading)
            vi_translation.append(translate_heading)

    return render_template("base.html", articles = vi_translation)



if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)