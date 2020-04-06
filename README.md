# AAPIVotes 2020

AAPIVotes 2020 is a full-stack application in an effort to  reduce language barriers for AAPI voters. To provide relevant news headlines to users, the app tokenizes the frequency of tweets used by leading presidential candidates. From those tokens, it aggregates nonpartisan news into one place, where users can have the option to translate it to any language of their choice. In addition, users can share articles via text message using Twilio and save articles they wish to revisit.


# Contents
 
 - Tech Stack
 - Features
 - Future State
 - Installation
 

## Tech Stack

API: Twitter, Twilio

Front End: JavaScript, HTML/CSS, jQuery&AJAX, Bootstrap

Back End: Python, Flask, Jinja, SQLAlchemy ORM, PostgreSQL

## Features
#### Landing Page

Users must first select a language that they wish to read in. If a language is not selected, the default setting is English. After the first visit, the app automatically saves the user's language preference for future visits - given that they are not viewing in incognito mode. Users can choose from the top 5 most frequently used words by all leading presidential candidates shown above. 

<a href="https://ibb.co/XJjzQjC"><img src="https://i.ibb.co/tCQbGQJ/Screen-Shot-2020-04-04-at-7-21-22-PM.png" alt="Screen-Shot-2020-04-04-at-7-21-22-PM" border="0"></a>

#### View Articles

This page renders articles from major news outlets that contain the keyword that the users chose from the landing page. The purpose is for them to get a quick overview of headlines including a description for each. If a user is interested in reading an article in its entirety, the hyperlink redirects them to the original source. 
In addition, users can save articles they wish to revisit. Once users click on the save button, it will fade out indicating that the article has been saved to "My Saved Articles" on the top right corner of the page. 

<a href="https://ibb.co/fYZkMCq"><img src="https://i.ibb.co/8DGrMjN/Screen-Shot-2020-04-04-at-7-27-03-PM.png" alt="Screen-Shot-2020-04-04-at-7-27-03-PM" border="0"></a>

#### Share Articles 
Users can also share articles by filling in the "Phone Number" form. The end-user will receive the message in the following format:

<a href="https://ibb.co/xzP9LmX"><img src="https://i.ibb.co/SVWYyQ5/Screenshot-2020-04-04-at-4-44-40-PM.jpg" alt="Screenshot-2020-04-04-at-4-44-40-PM" border="0"></a>

#### Save Articles
Users can view previously saved articles in their chosen language. SQLAlchemy ORM is used to query articles saved by a user's session id.  The hyperlink will redirect users to the original source where they can view the full content.
<a href="https://ibb.co/jRf8tyw"><img src="https://i.ibb.co/GTpdmWM/Screen-Shot-2020-04-04-at-7-28-36-PM.png" alt="Screen-Shot-2020-04-04-at-7-28-36-PM" border="0"></a># 

## Future State

The project roadmap for APPIVotes2020 has several features planned out for the next sprint:

 - Search option for saved articles
 - User's autonomy in choosing candidates 

## Installation
Clone or fork this repo:

```
https://github.com/quynhd07/translation2020.git

```

Create and activate a virtual environment inside your JobTracker directory:

```
virtualenv env
source env/bin/activate

```

Install the dependencies:

```
pip install -r requirements.txt

```

Sign up for Twilio and Twitter API keys then save your credentials to .bash. For example:
```
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
```


Set up the database:

```
createdb translation2020
python3 model.py
```

Run the app:

```
python3 server.py

```

You can now navigate to 'localhost:5000/' to access AAPIVotes2020.
