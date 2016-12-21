from django.shortcuts import render
import cgi
from django.http import HttpResponse
from django.template import Context
#import initial
# from initial import send_query
import process_twt

import sys
from nltk.twitter import Query, credsfromfile, TweetViewer
import numpy as np
import os
import pickle
sys.path.append('../mysite/sentiWebApp')
# print sys.path
from NBClassifier import NBClassifier
# initial

def evaluate_twt(tweets):
	print "score method called"
	with open(os.path.join(os.path.dirname(__file__), 'static/sentiWebApp/model','NBClassifier.pickle'), 'r') as f:
		
		NBC = pickle.load(f)
	score_list = NBC.test(tweets)
	print score_list
	return score_list

#evaluate_twt(['happy', 'sad'])

def send_query(keyword):
	# print "sendquery"
 
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
	# score_list = evaluate_twt(tweets) 
	# return str(score_list)
	for word in tweets:
	    final_tweets = final_tweets + word   
	
		# final_tweets = "final"
	return keyword + ":"+ final_tweets





# Create your views here.

def index(request):
	print("function 1 called")
	return render(request, "sentiWebApp/home.html")
def results(request):
	print("results method called")
	return render(request, "sentiWebApp/results.html")
	
def background_process(request):
	
	print("function 2 called !!!!!")
	if request.method == 'POST':
		newphrase = ""
		phrase_state = request.POST['phrase_state']
		#if string length is greater than 60, it is not a query request
		if len(phrase_state) < 60:
			# newphrase = initial.send_query(phrase_state)
			newphrase = send_query(phrase_state)
			print "query requested "
		else:
			if "Score: " in phrase_state and len (phrase_state) > 60: 
				newphrase = str(evaluate_twt(phrase_state))
			else:
				newphrase = process_twt.preprocess(phrase_state)

		# print(newphrase)	
		return HttpResponse(newphrase)
    # nothing went well
	return HttpResponse('FAIL!!!!!')
