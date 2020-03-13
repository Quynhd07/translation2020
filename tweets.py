import os 
from tweepy import OAuthHandler, API, Cursor
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer as wnl
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


def get_tweets() -> list:
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
            status = sub(r'https://t.co/\S+','', status)
            # add to list of tweets by account
            accounts[account].append(status)

    return accounts


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

    return all_tweets


def filter_tokens(tokens_list) -> list:
    """removes all stopsword and punctuation tokens from list of words"""
    filtered_tokens = []
    # create set of english stop words
    stop_words = set(stopwords.words('english'))
    # iterate though tokens list
    for token in tokens_list:
        # lemmatize (default pos is noun) and lowercase each token
        token = wnl().lemmatize(token).lower()
        # only add if it is not a stopword, punctuation, and longer than 3 chars 
        if token not in stop_words and token not in punctuation and len(token) > 3:
            filtered_tokens.append(token)

    return filtered_tokens
    

def get_frequent_tokens() -> list:
    """returns list of top 5 frequently used tokens"""
    # populate accounts by get_tweets; tokenize all tweets into list of unfiltered_tokens
    unfiltered_list = tokenize_tweets(get_tweets())
    # filter list of tokens
    filtered_list = filter_tokens(unfiltered_list)
    # create an object of FreqDist and return top 5 words
    frequency_count = FreqDist(filtered_list).most_common(5)
    top5_tokens = []
    for word, frequency in frequency_count:
        # add only the word in tuple to return_list 
        top5_tokens.append(word)

    return top5_tokens  




