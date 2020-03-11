import os 
from tweepy import OAuthHandler, API, Cursor
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from re import sub


consumer_key = os.getenv('translation_consumer_key')
consumer_secret = os.getenv('translation_consumer_secret')
access_token = os.getenv('translation_access_token')
access_token_secret = os.getenv('translation_access_token_secret')

# use OAuthHandler class to handle authentication (no callback url needed)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# API takes in authenication handler to be used; allows access to entire twitter restful api methods 
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


def get_tweets(accounts) -> list:
    """From list of accounts, get their 5 most recent tweets."""
    # iterate through list of accounts
    for account in accounts:
        # get each account's timeline of the last 5 tweets
        for status in Cursor(api.user_timeline,id=account, tweet_mode="extended").items(5):
            # check is status is a retweet, otherwise full text will be truncated
            if hasattr(status, 'retweeted_status'):
                status = status.retweeted_status
            # get full text of each status
            status = status.full_text
            # remove http link at the end
            status = sub(r' https://t.co/\S+','', status)
            # add to list of tweets by account
            accounts[account].append(status)

    return tokenize_tweets(accounts)


# tokenize tweets using NLTK 
def tokenize_tweets(accounts) -> list:
    """returns list of tokenized tweets of all users without stopword and punctuation tokens"""
    # create list to add tweets together 
    all_tweets = []
    # iterate through each account
    for account in accounts:
        # get list of tweets from each account
        tweets = accounts[account]
        # iterate through tweets for each account
        for tweet in tweets:
            all_tweets.extend(word_tokenize(tweet))

    return remove_stop_words(all_tweets)


def remove_stop_words(words_list) -> list:
    """removes all stopsword and punctuation tokens from list of words"""
    # create list of english stop words
    stop_words = set(stopwords.words('english'))
    # only add if it is not a stopword, punctuation, and longer than 3 chars 
    nonstop_words = [word for word in words_list if word not in stop_words and word not in punctuation and len(word) > 3]
    return nonstop_words
    

def get_frequent_words(words_list) -> list:
    """returns list of most used tokens"""
    return_list = []
    # create an object of FreqDist and return top 5 words
    frequency_count = FreqDist(words_list).most_common(5)
    for word, frequency in frequency_count:
        return_list.append(word)

    return return_list 




