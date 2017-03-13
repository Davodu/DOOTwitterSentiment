__author__ = 'Davies Odu'
from secrets import Oauth_Secrets
import tweepy
from textblob import TextBlob

def analyze(input_word):
    secrets = Oauth_Secrets()       
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)

    Num_tweets = 50                        
    Tweets = tweepy.Cursor(api.search, q=input_word).items(Num_tweets)
    negative,positive = (0.0,0.0)
    neg_count,pos_count = (0,0)
    neutral_count = 0

    for tweet in Tweets:
        # print tweet.text
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:         #Negative tweets
            negative += blob.sentiment.polarity
            neg_count += 1
        elif blob.sentiment.polarity == 0:      #Neutral tweets
            neutral_count += 1
        else:                                   #Positive tweets
            positive += blob.sentiment.polarity
            pos_count += 1
    return [['Category', 'Tweets crawled'],['Positive',pos_count]
            ,['Neutral',neutral_count],['Negative',neg_count]]