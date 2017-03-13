from django.shortcuts import render
from django.http import HttpResponse
from main_app import analyze
# Create your views here.

def index(request):
	return HttpResponse("Welcome")

def home(request):
	data = {"template_var": "Inject templates here....!!"}
	return render(request,"main_app/home.html",context=data)


def raw_tweets(request):
	word1 = request.POST["first_word"]
	word2 = request.POST["second_word"]
	data = analyze.analyze(word1)
	data2 = analyze.analyze(word2)
	# data example  [['Category', 'Tweets Crawled'], ['Positive', 18], ['Neutral', 23], ['Negative', 9]]
	return render(request, "main_app/raw_tweets.html", {'data': data,'data2':data2,'first_word':word1,'second_word':word2})




