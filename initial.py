# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
# from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import sys
from nltk.twitter import Query, credsfromfile, TweetViewer
import process_twt
import numpy as np
import os
import pickle
# sys.path.append('../mysite/sentiWebApp')
# print sys.path
from NBClassifier import NBClassifier

def evaluate_twt(tweets):
   	
	with open(os.path.join(os.path.dirname(__file__), 'static/sentiWebApp/model','NBClassifier.pickle'), 'r') as f:
		NBC = pickle.load(f)
	score_list = NBC.test(tweets)
    	print score_list
    	return score_list

evaluate_twt(['happy', 'sad'])

def send_query(keyword):
	print "initial.sendquery"
 
	oauth = credsfromfile()
	client = Query(**oauth)
	twtNum = 7
	client.register(TweetViewer(limit=twtNum))


	tweets_gen = client.search_tweets(keywords=keyword, limit=twtNum, lang='en')
	tweets = []
	# slangdict = process_twt.get_slang_dict()
	slangdict = {}
	count = 0
	final_tweets = " "
	for t in tweets_gen:
	    #append to tweets
	    temp = process_twt.preprocess(t['text'], slangdict=slangdict)
	    # tweets.append(str(count) + temp )
	    tweets.append(temp + ":")
	    count = count + 1  

	# test classifier 
	score_list = evaluate_twt(tweets) 
	return str(score_list)

	# for word in tweets:
	#     final_tweets = final_tweets + word   
	# return keyword + ":"+ final_tweets
	















