from flask import Flask, render_template, redirect, request, session, flash, Response
# from translate import Translator 
from googletrans import Translator
import tweets
from jinja2 import StrictUndefined
import os 
from sources import get_sources
from string import capwords
from model import ModelMixin, User, Article, User_article, db, connect_to_db
from twilio.rest import Client


app = Flask(__name__)
app.secret_key = os.getenv('translation2020_key')
twilio_test_sid = os.getenv('TWILIO_TEST_SID')
twilio_test_token = os.getenv('TWILIO_TEST_TOKEN')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
# set lifetime of cookie session 
app.SESSION_PERMANENT = True


@app.route('/')
def homepage():
    """displays list of most frequent tokens use can choose from"""
    # if first-time user, create new user and assign user_session to session id 
    if not session.get('id'):
        # create instance of user
        user = User(user_language='en')
        # save instance to database
        user.save()
        # add id property to flask session 
        session['id'] = user.user_session
        # default language property to English for first-time users 
        session['language'] = user.user_language
    # elif not session.get('language')
    #     user = User(user_language='en')
    #     user
    tokens = tweets.get_frequent_tokens()
    return render_template('homepage.html', tokens = tokens)

# TODO: change to post request 
@app.route('/save_lang_to_session')
def save_lang_to_session():
    """set new properties to flask session"""
    # get value of language form from homepage 
    language = request.args.get('language')
    print(language)
    # add language to their user_session in database 
    user = User.query.get(session['id'])
    user.user_language = language 
    # add langauge property to flask session 
    session['language'] = user.user_language
    user.save()
    return "Your preference has been saved."

# TODO: change to post request; implement AJAX
@app.route('/save_article')
def save_article():
    article_heading = request.args.get("heading")
    article_url = request.args.get("url")
    article = Article(article_heading=article_heading, article_url=article_url)
    article.save()
    user_article = User_article(user_session=session['id'], article_id=article.article_id)
    user_article.save()
    return Response(status = 200)


@app.route('/display_saved_articles')
def display_saved_article():
    user_articles = User_article.query.filter_by(user_session=session['id']).all()
    article_list = []
    url_list = []
    for ua in user_articles:
        article_list.append(ua.article.article_heading)
        url_list.append(ua.article.article_url)
    return render_template("saved.html", articles=zip(url_list,article_list))


@app.route('/share_article')
def share_article():
    article_heading = request.args.get("heading")
    article_url = request.args.get("url")
    article_description = request.args.get("description")
    phone_number = request.args.get("phone_number")
    client = Client(twilio_account_sid, twilio_auth_token)
    client.messages.create(body=article_heading + ':' + article_description + '\nCheck it out: ' + article_url,
                            from_='+18315315730', 
                            to=phone_number)
    return Response(status = 200)


@app.route('/<token>')
def display_key(token):
    """displays headlines"""
    # capitalize first letter to search in headings 
    token = capwords(token)
    # create instance of Translator 
    language = Translator()
    # get user's language 
    choice = session['language']

    # organize info into separate lists as they get translated  
    translated_headings = []
    translated_descriptions = []
    links = []
    # run the token to get relevant articles 
    sources = get_sources(token)
    # iterate through all sources and add to lists above 
    for i in range(0, len(sources)):
        for url, heading, description in zip(sources[i]['urls'],sources[i]['headings'], sources[i]['descriptions']):
            translated_headings.append(language.translate(heading, dest = choice).text)
            translated_descriptions.append(language.translate(description, dest = choice).text)
            links.append(url)

    return render_template("articles.html", articles_links=zip(links, translated_headings, translated_descriptions), token=token)




if __name__ == "__main__":
    connect_to_db(app)
    from flask_debugtoolbar import DebugToolbarExtension
    app.debug = True    
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)