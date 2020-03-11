import os 
from tweepy import OAuthHandler, API, Cursor
from collections import Counter 


consumer_key = os.getenv('translation_consumer_key')
consumer_secret = os.getenv('translation_consumer_secret')
access_token = os.getenv('translation_access_token')
access_token_secret = os.getenv('translation_access_token_secret')

# use OAuthHandler class to handle authentication (no callback url needed)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# call API class to access entire twitter restful api methods 
api = API(auth)

# dictionary containing last 5 tweets of each candidate
accounts = {
    'JoeBiden': [],
    'BernieSanders': [],
    'realDonaldTrump': [],
    'MikeBloomberg': [],
    'ElizabethWarren': [],
    'TulsiGabbard': []
}


def get_tweets(accounts_dict) -> dict:
    """From list of accounts, get their 5 most recent tweets."""
    # iterate through list of accounts
    for account in accounts:
        # get each account's timeline of the last 5 tweets
        for status in Cursor(api.user_timeline,id=account, tweet_mode="extended").items(5):
            # check is status is a retweet, otherwise full text will be truncated
            if hasattr(status, 'retweeted_status'):
                # add to list of tweets by account
                accounts[account].append(status.retweeted_status.full_text)
            # else, add tweet to list 
            else:
                accounts[account].append(status.full_text)
    return accounts


# tokenize tweets using NLTK or Counter




