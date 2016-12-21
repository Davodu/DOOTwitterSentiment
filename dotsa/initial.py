from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile
from pprint import pprint   #pretty print entire object
import sys
import pre_process

# get API information using credentials
oauth = credsfromfile() 
client = Query(**oauth)
tweets = client.search_tweets(keywords= 'nltk',limit = 10, lang = 'en') # generator
#tweet = next(tweets) #extract first tweet from the generator

slangmap = pre_process.init_slang_dict()

tweet_array = []

for twt in tweets: 
	print (pre_process.tokenize(twt['text'], slangmap=slangmap))
	# tweet_array.append(twt['text'])

# pre_process.tokenize(tweet_array, slangmap=slangmap) 


